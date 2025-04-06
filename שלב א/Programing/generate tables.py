import csv
import random
import faker

fake = faker.Faker()

# === 1. visiting_event.csv ===
def generate_visiting_events(filename, num_entries=1000):
    unique_pairs = set()
    while len(unique_pairs) < num_entries:
        pair = (random.randint(1, 1000), random.randint(1, 1000))
        unique_pairs.add(pair)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['resident_id', 'event_id'])
        for resident_id, event_id in unique_pairs:
            writer.writerow([resident_id, event_id])

# === 2. staff_member.csv ===
def generate_staff_members(filename, num_entries=1000):
    job_titles = ['Nurse', 'Doctor', 'Cleaner', 'Administrator', 'Therapist']
    used_names = set()

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['staff_member_id', 'staff_member_name', 'job_title'])
        for i in range(1, num_entries + 1):
            while True:
                name = fake.name()
                if name not in used_names:
                    used_names.add(name)
                    break
            title = random.choice(job_titles)
            writer.writerow([i, name, title])

# === 3. maintenance_req.csv ===
def generate_maintenance_requests(filename, num_entries=1000):
    statuses = ['received', 'taken care of', 'processed']
    used_rows = set()

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['request_id', 'room_id', 'staff_member_id', 'item_id', 'req_description', 'req_status'])
        for i in range(1, num_entries + 1):
            while True:
                room_id = random.randint(1, 1000)
                staff_id = random.randint(1, 1000)
                item_id = random.randint(0, 1000)
                description = fake.sentence(nb_words=6)
                status = random.choice(statuses)
                row_key = (room_id, staff_id, item_id, description, status)
                if row_key not in used_rows:
                    used_rows.add(row_key)
                    break
            writer.writerow([i, room_id, staff_id, item_id, description, status])

# === Generate CSVs ===
#generate_visiting_events('C:/Users/robin/OneDrive/Desktop/visiting_event.csv')
print("hi")
generate_staff_members('C:/Users/robin/OneDrive/Desktop/staff_member.csv')
generate_maintenance_requests('C:/Users/robin/OneDrive/Desktop/maintenance_req.csv')
