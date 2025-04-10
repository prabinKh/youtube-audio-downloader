# YouTube Audio Downloader

A Django-based web application that allows you to download audio from YouTube channels. The application automatically monitors YouTube channels for new content and downloads the audio files.

## Features

- Add and manage YouTube channels
- Automatic monitoring of channels for new content
- Download audio from YouTube videos
- Web-based interface for easy management
- Audio player and download functionality
- Real-time updates of channel content

## Prerequisites

- Python 3.x
- Django 5.2
- yt-dlp
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd youtube-audio-downloader
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r ytaudio/requirements.txt
```

4. Set up the database:

```bash
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

## Usage

1. Start the development server:

```bash
python manage.py runserver
```

2. Start the background tasks:

```bash
python manage.py checkupdateurls
python manage.py download_audio
```

3. Access the web interface at `http://localhost:8000`

## Background Tasks

The application uses two management commands that need to be running:

1. `checkupdateurls`: Monitors YouTube channels for new content
2. `download_audio`: Downloads audio from new videos

## Project Structure

- `downloader/`: Main application directory
  - `models.py`: Database models
  - `views.py`: View functions
  - `forms.py`: Form definitions
  - `utils.py`: Utility functions
  - `management/commands/`: Custom management commands
  - `templates/`: HTML templates
  - `static/`: Static files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django framework
- yt-dlp for YouTube downloading
- Bootstrap for UI components
- <img width="1676" alt="Screenshot 2025-04-10 at 12 08 07" src="https://github.com/user-attachments/assets/9ad3d089-238c-4ce5-929b-edcf95f4b85e" />

<img width="1599" alt="Screenshot 2025-04-10 at 12 08 54" src="https://github.com/user-attachments/assets/f70834a8-bfc9-4cb4-b996-de2f7ce1ea7e" />
