from locust import HttpUser, task, between
import random
import string

# Generate a random string of lowercase letters
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Generate a random list of keywords
def generate_random_keywords():
    num_keywords = random.randint(1, 4)
    keywords = []
    for i in range(num_keywords):
        keyword = generate_random_string(random.randint(3, 8))
        keywords.append(keyword)
    return keywords

# Generate a random query by combining random keywords and letters
def generate_random_query():
    keywords = generate_random_keywords()
    query = ''
    for keyword in keywords:
        query += keyword + ' '
    query += generate_random_string(random.randint(0, 5))
    return query.strip()

class ArticleUser(HttpUser):
    wait_time = between(1, 2.5)

    @task(1)
    def search_articles_not_random(self):
        query = "crema"
        self.client.get(f'/api/articles/?q={query}')
    
    @task(2)
    def search_articles_random(self):
        query = generate_random_query()
        self.client.get(f'/api/articles/?q={query}')