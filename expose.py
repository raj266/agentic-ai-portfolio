from pyngrok import ngrok
import time

# Set your authtoken from ngrok.com (free)
ngrok.set_auth_token("YOUR_TOKEN")

# Create tunnel to port 8000
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.disconnect()
