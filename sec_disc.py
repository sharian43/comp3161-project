from faker import Faker
import random

fake = Faker()

num_items = 10
item_id = 1
section_item_sql = ""

for _ in range(num_items):
    item_type = random.choice(['LECTURE_SLIDE', 'ASSIGNMENT'])
    # sectionID is left as NULL for now
    section_item_sql += f"INSERT INTO SectionItem (itemID, sectionID, item_type) VALUES ({item_id}, NULL, '{item_type}');\n"
    item_id += 1

print(section_item_sql)


