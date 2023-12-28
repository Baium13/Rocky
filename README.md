# How to deploy locally

1. Activate virtualenv

    ```shell
    python -m venv .venv && source .venv/bin/activate
    ```
2. Install everything
    
    ```shell
    pip install -r requirements.txt
    ```
3. Install migrations

    ```shell
    python manage.py migrate
    ```
