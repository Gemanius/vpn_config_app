# User Configuration Fetcher

This Python application fetches user configurations from an external panel, specifically the x-ui panel, and connects to a Telegram bot. Users can interact with the bot to retrieve details such as remaining time or capacity of their VPNs. The bot also provides command-line accessibility to the bot owner, whose details are configured in the `server_details.json` file.

## How it Works

The application is designed to retrieve user configurations from the x-ui panel and communicate with users via a Telegram bot. It utilizes the provided server details in the `server_details.json` file to establish connections and authenticate with the x-ui panel.

### Features

- Fetch user configurations from the x-ui panel.
- Interact with users via a Telegram bot.
- Provide command-line accessibility to the bot owner.

## Installation

1. Clone the project repository:

   ```bash
   git clone https://github.com/your-username/user-configuration-fetcher.git
   ```

2. Create a file named `server_details.json` with the following structure:

   ```json
   {
     "data": [
       {
         "username": "your_username",
         "password": "your_password",
         "ip": "x.x.x.x",
         "port": "your_port",
         "start_server_url": "your_start_server_url",
         "start_server_port": "your_start_server_port"
       }
     ],
     "TELEGRAM_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
     "CHAT_ID": "YOUR_TELEGRAM_CHAT_ID"
   }
   ```

   - Replace placeholders with your actual details:
     - `username`: Your username for the x-ui panel.
     - `password`: Your password for the x-ui panel.
     - `ip`: IP address of the x-ui panel.
     - `port`: Port number for the x-ui panel.
     - `start_server_url`: URL for starting the server.
     - `start_server_port`: Port for starting the server.
     - `TELEGRAM_TOKEN`: Token for your Telegram bot.
     - `CHAT_ID`: ID of the Telegram chat where the bot will operate.

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Python application:

```bash
python user_configuration_fetcher.py
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the x-ui panel and Telegram for their APIs.
- Special thanks to the community for feedback and contributions.
