Steps to deploy on Heroku


1. Install heroku CLI

2. Generate person access token on GitHub

3. Clone the project - `https://github.com/AnishShah/github-bot.git`

4. `heroku login`

5. `heroku create`

6. `git push heroku master` This will generate a URL where your app is deployed.

7. Set environment variables by running
   `heroku config:set ACCESS_TOKEN=<access_token>` (Paste the access token geenerate here)
   `heroku config:set SECRET_KEY=<secret_key>` (Add a secret key which will be used to authenticate GitHub webhooks payload)

8. Go to your project/organization on GitHub > Settings > Webhooks & services > Add Webhook

9. Payload URL will be the URL generated above.

10. Let me select individual events > Check `Pull Request`

11. Add Webhook.

To debug, you can check the logs using `heroku logs` command.
