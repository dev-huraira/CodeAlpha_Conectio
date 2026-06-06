"""
Management command to seed 100 dummy users with profile photos, banners, and details.
All passwords: 87654321
All emails: username@gmail.com
"""

import os
import urllib.request
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model

User = get_user_model()

# 100 realistic user profiles
DUMMY_USERS = [
    {"username": "sarah_chen", "first_name": "Sarah", "last_name": "Chen", "headline": "Senior Software Engineer at Google", "bio": "Passionate about building scalable systems and mentoring the next generation of engineers. Python, Go, and distributed systems enthusiast."},
    {"username": "james_wilson", "first_name": "James", "last_name": "Wilson", "headline": "Product Manager at Microsoft", "bio": "Driving product innovation through data-driven decisions. Previously at Amazon. MBA from Stanford."},
    {"username": "priya_sharma", "first_name": "Priya", "last_name": "Sharma", "headline": "UX Designer at Apple", "bio": "Creating intuitive experiences that delight users. Design thinking advocate. Speaker at design conferences worldwide."},
    {"username": "michael_brown", "first_name": "Michael", "last_name": "Brown", "headline": "Data Scientist at Netflix", "bio": "ML/AI enthusiast specializing in recommendation systems. PhD in Computer Science from MIT."},
    {"username": "emma_davis", "first_name": "Emma", "last_name": "Davis", "headline": "Marketing Director at Spotify", "bio": "Building brands that resonate. 10+ years in digital marketing and growth strategy."},
    {"username": "alex_rodriguez", "first_name": "Alex", "last_name": "Rodriguez", "headline": "Full Stack Developer at Meta", "bio": "React, Node.js, and everything in between. Open source contributor and tech blogger."},
    {"username": "olivia_johnson", "first_name": "Olivia", "last_name": "Johnson", "headline": "HR Manager at Deloitte", "bio": "People-first leader focused on building diverse and inclusive workplaces. SHRM certified."},
    {"username": "david_kim", "first_name": "David", "last_name": "Kim", "headline": "Startup Founder & CEO", "bio": "Building the future of fintech. YC W24 alum. Previously engineering lead at Stripe."},
    {"username": "sofia_martinez", "first_name": "Sofia", "last_name": "Martinez", "headline": "Graphic Designer | Freelancer", "bio": "Turning ideas into visual stories. Specializing in brand identity, illustration, and motion graphics."},
    {"username": "ryan_taylor", "first_name": "Ryan", "last_name": "Taylor", "headline": "DevOps Engineer at AWS", "bio": "Infrastructure as code enthusiast. Kubernetes, Terraform, and CI/CD pipelines. AWS Solutions Architect certified."},
    {"username": "emily_anderson", "first_name": "Emily", "last_name": "Anderson", "headline": "Content Strategist at HubSpot", "bio": "Crafting content that converts. SEO specialist and storytelling enthusiast. Published author."},
    {"username": "daniel_lee", "first_name": "Daniel", "last_name": "Lee", "headline": "iOS Developer at Uber", "bio": "Building mobile experiences for millions. Swift and SwiftUI expert. WWDC scholar."},
    {"username": "jessica_white", "first_name": "Jessica", "last_name": "White", "headline": "Financial Analyst at Goldman Sachs", "bio": "Analyzing markets and driving investment strategies. CFA charterholder. Passionate about financial literacy."},
    {"username": "chris_garcia", "first_name": "Chris", "last_name": "Garcia", "headline": "Cybersecurity Specialist at CrowdStrike", "bio": "Protecting organizations from cyber threats. CISSP certified. Bug bounty hunter on weekends."},
    {"username": "ashley_thomas", "first_name": "Ashley", "last_name": "Thomas", "headline": "Project Manager at Accenture", "bio": "PMP certified project manager delivering complex IT transformations. Agile and Scrum master."},
    {"username": "kevin_nguyen", "first_name": "Kevin", "last_name": "Nguyen", "headline": "Machine Learning Engineer at Tesla", "bio": "Working on autonomous driving and computer vision. Published researcher in NeurIPS and ICML."},
    {"username": "rachel_clark", "first_name": "Rachel", "last_name": "Clark", "headline": "Nurse Practitioner at Mayo Clinic", "bio": "Dedicated to patient care and health education. DNP graduate. Advocate for healthcare accessibility."},
    {"username": "marcus_jones", "first_name": "Marcus", "last_name": "Jones", "headline": "Sales Director at Salesforce", "bio": "Helping businesses grow through technology. 15 years in enterprise sales. Mentor and coach."},
    {"username": "natalie_moore", "first_name": "Natalie", "last_name": "Moore", "headline": "Environmental Scientist at EPA", "bio": "Researching climate change solutions. PhD in Environmental Science. Passionate about sustainability."},
    {"username": "brandon_jackson", "first_name": "Brandon", "last_name": "Jackson", "headline": "Mechanical Engineer at SpaceX", "bio": "Designing systems that push the boundaries of space exploration. Rocket propulsion specialist."},
    {"username": "samantha_harris", "first_name": "Samantha", "last_name": "Harris", "headline": "Attorney at Kirkland & Ellis", "bio": "Corporate law specialist focusing on M&A and securities. Harvard Law graduate. Pro bono advocate."},
    {"username": "tyler_martin", "first_name": "Tyler", "last_name": "Martin", "headline": "Blockchain Developer", "bio": "Building decentralized applications on Ethereum and Solana. Smart contract auditor. Web3 evangelist."},
    {"username": "hannah_wright", "first_name": "Hannah", "last_name": "Wright", "headline": "Elementary School Teacher", "bio": "Shaping young minds and making learning fun. National Board Certified. EdTech enthusiast."},
    {"username": "jordan_lopez", "first_name": "Jordan", "last_name": "Lopez", "headline": "Video Producer at YouTube", "bio": "Creating compelling video content that reaches millions. Expert in storytelling and post-production."},
    {"username": "megan_hill", "first_name": "Megan", "last_name": "Hill", "headline": "Nutritionist & Wellness Coach", "bio": "Helping people achieve their health goals through science-based nutrition. Registered Dietitian."},
    {"username": "andrew_scott", "first_name": "Andrew", "last_name": "Scott", "headline": "Architect at Gensler", "bio": "Designing sustainable buildings that inspire. LEED certified. Winner of AIA Design Awards."},
    {"username": "lauren_green", "first_name": "Lauren", "last_name": "Green", "headline": "Social Media Manager at Nike", "bio": "Building communities and driving engagement across platforms. 5M+ followers managed collectively."},
    {"username": "jason_adams", "first_name": "Jason", "last_name": "Adams", "headline": "Cloud Solutions Architect at Azure", "bio": "Designing enterprise cloud infrastructure. 8x Microsoft certified. Speaker and technical writer."},
    {"username": "stephanie_baker", "first_name": "Stephanie", "last_name": "Baker", "headline": "Psychologist | Private Practice", "bio": "Specializing in cognitive behavioral therapy. PhD in Clinical Psychology. Author of 'Mind Over Matter'."},
    {"username": "nick_gonzalez", "first_name": "Nick", "last_name": "Gonzalez", "headline": "Chef & Restaurant Owner", "bio": "Michelin-trained chef bringing farm-to-table dining to the city. Cookbook author. Food Network featured."},
    {"username": "victoria_nelson", "first_name": "Victoria", "last_name": "Nelson", "headline": "Venture Capital Associate at a16z", "bio": "Investing in the next generation of transformative startups. Focus on AI, biotech, and climate tech."},
    {"username": "matt_carter", "first_name": "Matt", "last_name": "Carter", "headline": "Sports Journalist at ESPN", "bio": "Covering NBA and NFL. Storyteller at heart. Emmy nominated. Podcast host of 'The Sports Desk'."},
    {"username": "amanda_mitchell", "first_name": "Amanda", "last_name": "Mitchell", "headline": "Pharmaceutical Researcher at Pfizer", "bio": "Drug discovery and clinical trials. PhD in Biochemistry. Published 30+ peer-reviewed papers."},
    {"username": "brian_perez", "first_name": "Brian", "last_name": "Perez", "headline": "Civil Engineer at AECOM", "bio": "Infrastructure design for smart cities. PE licensed. Working on sustainable transportation projects."},
    {"username": "katherine_roberts", "first_name": "Katherine", "last_name": "Roberts", "headline": "Fashion Designer | Independent", "bio": "Sustainable fashion advocate. Featured in Vogue and Elle. Creating timeless pieces with ethical materials."},
    {"username": "sean_turner", "first_name": "Sean", "last_name": "Turner", "headline": "Backend Engineer at Airbnb", "bio": "Building reliable services at scale. Java, Kotlin, and microservices architecture. System design enthusiast."},
    {"username": "melissa_phillips", "first_name": "Melissa", "last_name": "Phillips", "headline": "Event Planner & Coordinator", "bio": "Creating unforgettable experiences for corporate and private events. 200+ successful events organized."},
    {"username": "trevor_campbell", "first_name": "Trevor", "last_name": "Campbell", "headline": "Photojournalist at National Geographic", "bio": "Documenting stories from around the world. Award-winning photographer. Conservation advocate."},
    {"username": "nicole_parker", "first_name": "Nicole", "last_name": "Parker", "headline": "Supply Chain Manager at Amazon", "bio": "Optimizing global logistics and fulfillment operations. Six Sigma Black Belt. MBA from Wharton."},
    {"username": "derek_evans", "first_name": "Derek", "last_name": "Evans", "headline": "Music Producer | Grammy Nominated", "bio": "Crafting sounds that move people. Worked with top artists across hip-hop, pop, and R&B genres."},
    {"username": "christina_edwards", "first_name": "Christina", "last_name": "Edwards", "headline": "Pediatrician at Children's Hospital", "bio": "Dedicated to children's health and wellness. Board certified. Medical school faculty member."},
    {"username": "jake_collins", "first_name": "Jake", "last_name": "Collins", "headline": "Game Developer at Riot Games", "bio": "Creating immersive gaming experiences. Unity and Unreal Engine expert. Indie game jam winner."},
    {"username": "alyssa_stewart", "first_name": "Alyssa", "last_name": "Stewart", "headline": "Real Estate Agent at Keller Williams", "bio": "Helping families find their dream homes. Top 1% agent nationally. Investment property specialist."},
    {"username": "adam_sanchez", "first_name": "Adam", "last_name": "Sanchez", "headline": "Electrical Engineer at Intel", "bio": "Chip design and semiconductor technology. 12 patents filed. Working on next-gen processor architectures."},
    {"username": "tiffany_morris", "first_name": "Tiffany", "last_name": "Morris", "headline": "Dental Surgeon | Private Practice", "bio": "Cosmetic and restorative dentistry. DDS from Columbia. Committed to making smiles beautiful."},
    {"username": "ethan_rogers", "first_name": "Ethan", "last_name": "Rogers", "headline": "Aerospace Engineer at Boeing", "bio": "Designing the next generation of commercial aircraft. MS in Aerospace Engineering from Caltech."},
    {"username": "zoe_reed", "first_name": "Zoe", "last_name": "Reed", "headline": "Illustrator & Children's Book Author", "bio": "Creating worlds through art and words. 15 published books. New York Times bestselling illustrator."},
    {"username": "lucas_cook", "first_name": "Lucas", "last_name": "Cook", "headline": "Quantitative Analyst at Citadel", "bio": "Mathematical modeling for trading strategies. PhD in Applied Mathematics. Python and R expert."},
    {"username": "grace_morgan", "first_name": "Grace", "last_name": "Morgan", "headline": "Physical Therapist at HSS", "bio": "Helping athletes recover and perform at their best. DPT graduate. Sports rehabilitation specialist."},
    {"username": "connor_bell", "first_name": "Connor", "last_name": "Bell", "headline": "Filmmaker & Director", "bio": "Independent films that challenge perspectives. Sundance selection. Currently producing a documentary series."},
    {"username": "kayla_murphy", "first_name": "Kayla", "last_name": "Murphy", "headline": "Operations Manager at FedEx", "bio": "Streamlining logistics for maximum efficiency. Lean management certified. Leading digital transformation."},
    {"username": "dylan_rivera", "first_name": "Dylan", "last_name": "Rivera", "headline": "Frontend Developer at Shopify", "bio": "Crafting pixel-perfect user interfaces. Vue.js and React specialist. Accessibility advocate."},
    {"username": "isabella_cooper", "first_name": "Isabella", "last_name": "Cooper", "headline": "Marine Biologist at NOAA", "bio": "Studying ocean ecosystems and coral reef conservation. PhD in Marine Biology. Scuba diving instructor."},
    {"username": "logan_richardson", "first_name": "Logan", "last_name": "Richardson", "headline": "Podcast Host & Media Entrepreneur", "bio": "Founder of a top-50 tech podcast with 2M+ downloads. Interviewing industry leaders and innovators."},
    {"username": "chloe_cox", "first_name": "Chloe", "last_name": "Cox", "headline": "Interior Designer at Studio McGee", "bio": "Transforming spaces into homes. Residential and commercial design. Featured on Netflix and HGTV."},
    {"username": "nathan_howard", "first_name": "Nathan", "last_name": "Howard", "headline": "Paramedic & EMT Instructor", "bio": "First responder saving lives daily. 10+ years of emergency medicine. Training the next generation of EMTs."},
    {"username": "madison_ward", "first_name": "Madison", "last_name": "Ward", "headline": "Account Executive at Oracle", "bio": "Enterprise software sales pro. Consistently exceeding quotas. Building lasting client relationships."},
    {"username": "hunter_torres", "first_name": "Hunter", "last_name": "Torres", "headline": "Personal Trainer & Fitness Coach", "bio": "NASM certified trainer helping clients transform their lives. Online coaching program with 500+ clients."},
    {"username": "lily_peterson", "first_name": "Lily", "last_name": "Peterson", "headline": "Translator & Interpreter", "bio": "Fluent in English, Spanish, French, and Mandarin. UN conference interpreter. Literary translator."},
    {"username": "austin_gray", "first_name": "Austin", "last_name": "Gray", "headline": "Robotics Engineer at Boston Dynamics", "bio": "Building robots that navigate the real world. MS in Robotics from CMU. ROS and SLAM specialist."},
    {"username": "aria_ramirez", "first_name": "Aria", "last_name": "Ramirez", "headline": "Journalist at The Washington Post", "bio": "Investigative reporting on politics and social issues. Pulitzer Prize finalist. Columbia J-School grad."},
    {"username": "cole_james", "first_name": "Cole", "last_name": "James", "headline": "Brewmaster & Craft Beer Entrepreneur", "bio": "Founder of a craft brewery with 15 award-winning recipes. Beer judge certified. Brewing science grad."},
    {"username": "nora_watson", "first_name": "Nora", "last_name": "Watson", "headline": "Occupational Therapist", "bio": "Helping individuals regain independence and quality of life. Pediatric OT specialist. Sensory integration expert."},
    {"username": "ian_brooks", "first_name": "Ian", "last_name": "Brooks", "headline": "Tax Attorney at PwC", "bio": "International tax planning and compliance. JD/LLM in Taxation. Advising Fortune 500 companies."},
    {"username": "paige_kelly", "first_name": "Paige", "last_name": "Kelly", "headline": "Veterinarian | Animal Hospital", "bio": "Caring for pets and their families. DVM from UC Davis. Emergency and critical care specialist."},
    {"username": "mason_sanders", "first_name": "Mason", "last_name": "Sanders", "headline": "QA Engineer at Atlassian", "bio": "Ensuring software quality through automation. Selenium, Cypress, and performance testing expert."},
    {"username": "brooke_price", "first_name": "Brooke", "last_name": "Price", "headline": "Digital Marketing Consultant", "bio": "Helping startups grow from 0 to 1M users. PPC, SEO, and conversion optimization. Google Ads certified."},
    {"username": "eli_bennett", "first_name": "Eli", "last_name": "Bennett", "headline": "Structural Engineer at WSP", "bio": "Designing earthquake-resistant structures. PE licensed. Working on iconic skyscraper projects worldwide."},
    {"username": "ruby_wood", "first_name": "Ruby", "last_name": "Wood", "headline": "Yoga Instructor & Wellness Blogger", "bio": "RYT-500 certified yoga teacher. Mindfulness and meditation guide. Wellness content creator with 100K followers."},
    {"username": "gavin_barnes", "first_name": "Gavin", "last_name": "Barnes", "headline": "Embedded Systems Engineer at NVIDIA", "bio": "GPU programming and hardware-software co-design. CUDA specialist. Working on AI accelerators."},
    {"username": "maya_ross", "first_name": "Maya", "last_name": "Ross", "headline": "Museum Curator at The Met", "bio": "Bringing art and culture to life. PhD in Art History. Specializing in contemporary and modern art."},
    {"username": "blake_henderson", "first_name": "Blake", "last_name": "Henderson", "headline": "Pilot at Delta Air Lines", "bio": "Commercial airline pilot with 8000+ flight hours. ATP rated. Former Air Force pilot."},
    {"username": "fiona_coleman", "first_name": "Fiona", "last_name": "Coleman", "headline": "Speech Therapist | Children's Clinic", "bio": "Helping children find their voice. MS in Speech-Language Pathology. Early intervention specialist."},
    {"username": "owen_jenkins", "first_name": "Owen", "last_name": "Jenkins", "headline": "Sustainability Consultant at McKinsey", "bio": "Advising companies on ESG strategy and carbon reduction. MBA with focus on sustainable business."},
    {"username": "claire_perry", "first_name": "Claire", "last_name": "Perry", "headline": "Opera Singer & Voice Coach", "bio": "Soprano performing at major opera houses worldwide. Juilliard graduate. Private voice instruction."},
    {"username": "reid_powell", "first_name": "Reid", "last_name": "Powell", "headline": "Database Administrator at MongoDB", "bio": "Managing data at scale. MongoDB, PostgreSQL, and Redis expert. Performance tuning specialist."},
    {"username": "elise_long", "first_name": "Elise", "last_name": "Long", "headline": "Social Worker | Community Outreach", "bio": "Advocating for vulnerable populations. MSW from University of Michigan. Mental health first aid trainer."},
    {"username": "miles_patterson", "first_name": "Miles", "last_name": "Patterson", "headline": "Sound Engineer at Abbey Road Studios", "bio": "Mixing and mastering for top recording artists. Grammy-winning engineer. Audio technology innovator."},
    {"username": "sienna_hughes", "first_name": "Sienna", "last_name": "Hughes", "headline": "Biomedical Engineer at Medtronic", "bio": "Developing life-saving medical devices. MS in Biomedical Engineering. 8 patents in cardiac technology."},
    {"username": "max_foster", "first_name": "Max", "last_name": "Foster", "headline": "Stand-up Comedian & Writer", "bio": "Making people laugh for a living. Netflix special. Head writer on a late-night show. Touring globally."},
    {"username": "ivy_gonzales", "first_name": "Ivy", "last_name": "Gonzales", "headline": "Epidemiologist at WHO", "bio": "Tracking and preventing disease outbreaks globally. PhD in Epidemiology. Published in The Lancet."},
    {"username": "levi_simmons", "first_name": "Levi", "last_name": "Simmons", "headline": "Carpenter & Furniture Maker", "bio": "Handcrafted custom furniture and woodworking. Third-generation craftsman. Featured in Architectural Digest."},
    {"username": "piper_alexander", "first_name": "Piper", "last_name": "Alexander", "headline": "Public Relations Director at Edelman", "bio": "Crisis management and brand communications. 12 years in PR. Cannes Lions winner."},
    {"username": "oscar_russell", "first_name": "Oscar", "last_name": "Russell", "headline": "Climatologist at NASA", "bio": "Studying Earth's climate system using satellite data. PhD from Columbia. Science communicator."},
    {"username": "harper_griffin", "first_name": "Harper", "last_name": "Griffin", "headline": "Midwife & Prenatal Educator", "bio": "Supporting families through pregnancy and birth. CNM certified. Natural childbirth advocate."},
    {"username": "cal_hayes", "first_name": "Cal", "last_name": "Hayes", "headline": "Technical Writer at Stripe", "bio": "Making complex APIs understandable. Documentation that developers actually enjoy reading."},
    {"username": "stella_butler", "first_name": "Stella", "last_name": "Butler", "headline": "Sommelier & Wine Educator", "bio": "Master Sommelier candidate. Wine director at a Michelin-starred restaurant. Wine column contributor."},
    {"username": "theo_barnes", "first_name": "Theo", "last_name": "Barnes", "headline": "Urban Planner at City Hall", "bio": "Designing livable cities for the future. AICP certified. Focus on public transit and green spaces."},
    {"username": "gemma_flores", "first_name": "Gemma", "last_name": "Flores", "headline": "Dance Choreographer & Studio Owner", "bio": "Contemporary and hip-hop choreography. Worked with top music artists. Training dancers for 15+ years."},
    {"username": "finn_russell", "first_name": "Finn", "last_name": "Russell", "headline": "Ethical Hacker & Security Researcher", "bio": "Finding vulnerabilities before the bad guys do. OSCP certified. Bug bounty hunter with $500K+ earned."},
    {"username": "vivian_cruz", "first_name": "Vivian", "last_name": "Cruz", "headline": "Immigration Attorney", "bio": "Helping families navigate the immigration system. JD from Georgetown. Fluent in English and Spanish."},
    {"username": "otto_webb", "first_name": "Otto", "last_name": "Webb", "headline": "Agricultural Engineer & Farmer", "bio": "Combining technology and farming for sustainable agriculture. Precision farming specialist. 500-acre operation."},
    {"username": "nina_stone", "first_name": "Nina", "last_name": "Stone", "headline": "Makeup Artist & Beauty Influencer", "bio": "Celebrity makeup artist with 2M followers. Brand collaborations with major cosmetics companies. YouTube creator."},
    {"username": "wade_fisher", "first_name": "Wade", "last_name": "Fisher", "headline": "Firefighter & Paramedic", "bio": "Serving the community for 12 years. Hazmat certified. Training officer and youth fire safety educator."},
    {"username": "serena_washington", "first_name": "Serena", "last_name": "Washington", "headline": "Political Campaign Strategist", "bio": "Winning campaigns through data-driven strategy. 20+ successful campaigns. Political analysis contributor on CNN."},
    {"username": "jude_hart", "first_name": "Jude", "last_name": "Hart", "headline": "Tattoo Artist & Studio Owner", "bio": "Custom tattoo design and fine line work. International tattoo convention winner. 10K+ satisfied clients."},
    {"username": "freya_mills", "first_name": "Freya", "last_name": "Mills", "headline": "Astrophysicist at MIT", "bio": "Studying exoplanets and the search for extraterrestrial life. PhD from Cambridge. TEDx speaker."},
    {"username": "kai_warren", "first_name": "Kai", "last_name": "Warren", "headline": "Surf Instructor & Ocean Conservationist", "bio": "Teaching people to ride waves and respect the ocean. ISA certified. Beach cleanup organizer."},
    {"username": "luna_diaz", "first_name": "Luna", "last_name": "Diaz", "headline": "Ceramic Artist & Potter", "bio": "Handmade pottery and ceramic art. Gallery exhibitions worldwide. Teaching workshops in my studio."},
]

# Website URLs for some users
WEBSITES = [
    "github.com/sarahchen", "jameswilson.com", "priyauxdesign.com", "michaelbrown.dev",
    "emmadavismarketing.com", "alexrodriguez.io", "", "davidkim.vc", "sofiamartinez.art",
    "ryantaylor.cloud", "emilywrites.com", "daniellee.dev", "", "chrisgarcia.security",
    "", "kevinnguyen.ml", "", "saleswithmarcus.com", "", "",
    "samanthaharris.law", "tylercrypto.dev", "hannahteaches.com", "jordanlopez.tv",
    "meganhill.health", "andrewscott.design", "laurengreen.social", "jasonadams.cloud",
    "drstephaniebaker.com", "chefnick.com", "victorianelson.vc", "mattcartersports.com",
    "", "", "katherinerobertsfashion.com", "seanturner.dev", "melissaphillipsevents.com",
    "trevorcampbell.photo", "", "derekevansmusic.com", "drchristina.com", "jakecollins.games",
    "alyssahomes.com", "", "drtiffanymorris.com", "", "zoereedart.com",
    "", "gracemorganpt.com", "connorbellfilms.com", "", "dylanrivera.dev",
    "", "loganrichardson.fm", "chloeinteriors.com", "", "",
    "huntertorres.fitness", "lilypeterson.com", "austingray.tech", "ariaramirez.press",
    "colebrews.com", "", "ianbrookslaw.com", "drpaigekelly.vet", "",
    "brookeprice.marketing", "", "rubywellness.com", "", "",
    "blakeflies.com", "", "", "claireperryopera.com", "",
    "eliselong.org", "", "", "maxfosterlaughs.com", "",
    "levisimmons.craft", "piperpr.com", "", "", "calhayeswrites.dev",
    "stellawines.com", "", "", "", "viviancruzelaw.com",
    "ottofarms.com", "ninastonebeauty.com", "", "", "judehart.ink",
    "freyamills.science", "kaiwarren.surf", "lunadiaz.art",
]


class Command(BaseCommand):
    help = 'Seed 100 dummy users with profile photos, banners, and details'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete ALL existing users and posts before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Deleting all existing users and posts...'))
            User.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All users and posts deleted.'))

        created_count = 0
        skipped_count = 0

        for i, user_data in enumerate(DUMMY_USERS):
            username = user_data['username']
            email = f"{username}@gmail.com"

            if User.objects.filter(username=username).exists():
                skipped_count += 1
                self.stdout.write(f'  Skipping {username} (already exists)')
                continue

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='87654321',
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                headline=user_data.get('headline', ''),
                bio=user_data.get('bio', ''),
            )

            # Set website if available
            website = WEBSITES[i] if i < len(WEBSITES) else ''
            if website:
                user.website = f'https://{website}'
                user.save(update_fields=['website'])

            # Download and set avatar from DiceBear API
            try:
                avatar_url = f'https://api.dicebear.com/7.x/lorelei/png?seed={username}&size=200'
                req = urllib.request.Request(avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req, timeout=10)
                avatar_data = response.read()
                user.avatar.save(
                    f'{username}_avatar.png',
                    ContentFile(avatar_data),
                    save=True
                )
                self.stdout.write(f'  ✓ Avatar saved for {username}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Avatar failed for {username}: {e}'))

            # Download and set banner from picsum
            try:
                banner_url = f'https://picsum.photos/seed/{username}/1200/400'
                req = urllib.request.Request(banner_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req, timeout=10)
                banner_data = response.read()
                user.banner.save(
                    f'{username}_banner.jpg',
                    ContentFile(banner_data),
                    save=True
                )
                self.stdout.write(f'  ✓ Banner saved for {username}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Banner failed for {username}: {e}'))

            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f'[{created_count}/100] Created: {user.first_name} {user.last_name} (@{username})'
            ))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done! Created {created_count} users, skipped {skipped_count}.'))
        self.stdout.write(self.style.SUCCESS(f'All passwords: 87654321'))
        self.stdout.write(self.style.SUCCESS(f'All emails: username@gmail.com'))
