"""
Management command to seed at least 1 post per user.
Creates realistic, professional posts matching each user's headline/job.
Downloads high-quality random images for a subset of posts.
"""

import os
import random
import urllib.request
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

# Category-specific post templates
TECH_TEMPLATES = [
    "Just spent 3 hours refactoring a legacy module. Reduced the codebase by 200 lines and made it 3x faster. Clean code is quiet code! 💻✨",
    "What is your preferred database when building scalable microservices? I've been leaning heavily towards PostgreSQL lately for its reliability, but MongoDB still has its place. Thoughts?",
    "Don't write comments explaining *what* the code does. Write comments explaining *why* you did it that way. Future you will thank you.",
    "Had an interesting debate with my team today: Monolith vs Microservices. For early-stage startups, a modular monolith is almost always the right answer. Don't overengineer too early!",
    "Learning a new programming language or framework is great, but mastering core software design patterns, data structures, and algorithms is what actually makes you a better engineer.",
    "Just automated a manual deployment task that used to take 30 minutes. Now it runs on a GitHub Action in under 90 seconds. Automation for the win! 🚀",
]

DESIGN_TEMPLATES = [
    "Good design is invisible. It guides the user naturally without them realizing they are being guided. Simplicity is the ultimate sophistication. 🎨✨",
    "Working on a new brand identity project today. Choosing the right color palette is always the most therapeutic yet challenging part. Here is a sneak peek of the moodboard!",
    "Designers: Stop designing for other designers. Design for the users who actually use your product every day. Empathy is your superpower.",
    "Spent the morning auditing our app's accessibility. Color contrast ratios, screen reader compatibility, and keyboard navigation. Inclusivity isn't a feature; it's a foundation.",
    "Had a great session feedback review with a client today. Iteration is where the magic happens. Don't fall in love with your first draft!",
]

LEADERSHIP_TEMPLATES = [
    "Prioritization is the hardest part of product management. Saying 'no' to good ideas is the only way to say 'yes' to the great ones. Focus is key. 🚀",
    "Met with our users today for a feedback session. It's incredibly humbling to see how people interact with what we build. Step away from your dashboards and talk to real humans!",
    "The best managers don't manage work; they build trust, clear roadblocks, and empower their teams to do their best work. Lead with empathy.",
    "Excited to share that we just launched our new product roadmap! Thanks to the incredible engineering and design teams for making this happen. Big things ahead!",
    "Startup advice: Build something people want. It sounds simple, but it's incredibly easy to get distracted by shiny features that nobody actually uses.",
]

HEALTH_TEMPLATES = [
    "A friendly reminder to take a step back, drink some water, and stretch. Your physical and mental well-being should always be your top priority. Take care of yourself! 🩺",
    "Had a great discussion today about the intersection of AI and modern medicine. Technology will never replace human empathy, but it can certainly help us treat patients more efficiently.",
    "Grateful for the incredible healthcare team I work with every day. Medicine can be challenging, but making a positive impact on patients' lives makes it all worth it.",
    "Wellness is not a destination; it's a daily practice. What small step are you taking today to improve your health?",
]

WRITER_TEMPLATES = [
    "Writing is thinking. If you can't explain a complex concept simply, you don't understand it well enough yet. Keep editing. ✍️",
    "Just finished drafting the chapter for my upcoming book/documentation. The first draft is just you telling yourself the story. The real work starts in revision.",
    "Content strategy isn't just about creating more content; it's about creating the right content for the right audience at the right time.",
]

GENERAL_TEMPLATES = [
    "Success isn't about avoiding failure; it's about learning from it and moving forward. Keep pushing, keep learning, and keep growing. Happy Monday everyone! 🙌",
    "Networking isn't about collecting contacts; it's about planting relations. Grateful for the amazing people I've met through this platform. Let's connect!",
    "Had a very productive planning session today. Setting clear goals for the week is the best way to stay focused and avoid burnout. What are your goals for this week?",
    "Every accomplishments starts with the decision to try. Don't let the fear of failure keep you from starting your journey.",
]


class Command(BaseCommand):
    help = 'Seed at least 1 realistic post per user, matching their profession'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing posts before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Deleting all existing posts...'))
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All posts deleted.'))

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR('No users found in database! Please run seed_users first.'))
            return

        self.stdout.write(f'Found {users.count()} users. Generating posts...')

        created_count = 0

        for user in users:
            # Skip superusers unless they want posts for them too (let's add a post for them anyway)
            headline = user.headline.lower()
            bio = user.bio.lower()

            # Categorize user to select the best template
            if any(w in headline or w in bio for w in ['engineer', 'developer', 'programmer', 'tech', 'software', 'devops', 'cloud', 'data scientist', 'machine learning', 'robotics']):
                templates = TECH_TEMPLATES
            elif any(w in headline or w in bio for w in ['designer', 'artist', 'potter', 'ceramic', 'illustrator', 'creative', 'ux', 'ui', 'brand', 'interior']):
                templates = DESIGN_TEMPLATES
            elif any(w in headline or w in bio for w in ['manager', 'founder', 'ceo', 'director', 'lead', 'venture', 'president', 'vp']):
                templates = LEADERSHIP_TEMPLATES
            elif any(w in headline or w in bio for w in ['doctor', 'nurse', 'practitioner', 'dentist', 'pediatrician', 'physiologist', 'therapist', 'vet', 'veterinarian', 'health']):
                templates = HEALTH_TEMPLATES
            elif any(w in headline or w in bio for w in ['writer', 'author', 'journalist', 'editor', 'content', 'pr', 'public relations']):
                templates = WRITER_TEMPLATES
            else:
                templates = GENERAL_TEMPLATES

            # Choose a random post template from the selected category
            content = random.choice(templates)

            # Create the Post object
            post = Post(
                author=user,
                content=content
            )

            # Decide if we attach an image (approx 30% of posts get an image)
            attach_image = random.random() < 0.35
            
            if attach_image:
                try:
                    # Get a beautiful high-quality image from Picsum
                    # Using a random seed based on username for consistency
                    image_url = f'https://picsum.photos/seed/{user.username}_post/800/600'
                    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    response = urllib.request.urlopen(req, timeout=10)
                    image_data = response.read()
                    
                    post.image.save(
                        f'{user.username}_post_img.jpg',
                        ContentFile(image_data),
                        save=False  # Save after database insert
                    )
                    image_status = "with image"
                except Exception as e:
                    image_status = f"failed to load image ({e})"
            else:
                image_status = "text-only"

            post.save()
            
            # Sync posts_count cache on the user if model has it
            if hasattr(user, 'posts_count'):
                user.posts_count = user.posts.count()
                user.save(update_fields=['posts_count'])

            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f'[{created_count}] Created post for @{user.username} ({image_status})'
            ))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully seeded {created_count} posts (one per user)! 🚀'))
