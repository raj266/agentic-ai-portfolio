from pyngrok import ngrok
import time

# Set your authtoken from ngrok.com (free)
ngrok.set_auth_token("3Bf5tFICys1Jd29KtSiej6gpqoE_5R3PEcdZCetc8SGEgbAMU")

# Create tunnel to port 8000
public_url = ngrok.connect(8000)
print(f"Public URL: {public_url}")

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.disconnect()