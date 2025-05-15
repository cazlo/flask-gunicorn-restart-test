# locustfile.py
import time
from locust import HttpUser, task, between, constant_pacing, events
from locust.runners import MasterRunner

# Target rate (requests per second)
TARGET_RPS = 10

class FlaskAppUser(HttpUser):
    # Set wait time to achieve 10 RPS constant rate
    wait_time = constant_pacing(1 / TARGET_RPS)  # 1/10 = 0.1 seconds between requests

    # Define tasks that the user will execute
    @task(3)  # Higher weight for the main endpoint
    def index_page(self):
        self.client.get("/")
        
    @task(1)  # Lower weight for the health endpoint
    def health_check(self):
        self.client.get("/health")

# Optional: Add a listener to print the current RPS during the test
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(f"Starting test to achieve {TARGET_RPS} requests per second")
    
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """Log request statistics to track actual RPS"""
    # This function will be called for every request made
    # You can implement custom logging/tracking here if needed
    pass

# Custom stats printer to show current RPS
@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    print(f"Spawning complete: {user_count} users")
    print(f"Target RPS: {TARGET_RPS}")
    print("Test is now running at constant rate")
    
# Add a custom command line option for setting the RPS
def command_line_parser(parser):
    parser.add_argument(
        "--rps", 
        type=float,
        env_var="LOCUST_RPS", 
        default=TARGET_RPS,
        help="Target requests per second"
    )

# If the file is the main module, this will be executed
if __name__ == "__main__":
    # Command line: locust -f locustfile.py --headless -u 10 -r 1 -t 60s --host=http://localhost:8000
    print("Run Locust with: locust -f locustfile.py --host=http://localhost:8000")
