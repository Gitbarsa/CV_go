#!/usr/bin/env python3
"""
CV Automation MVP - Build Script
Auto-generates tailored CVs and uploads to Google Drive
Optional: Fetch Job Descriptions from Notion DB
"""

import argparse
import json
import os
from pathlib import Path
from jinja2 import Template
from notion_client import Client
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


# Base directory
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"


def load_profile():
    """Load profile data from JSON file"""
    profile_path = DATA_DIR / "profile.json"
    with open(profile_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_jd_from_notion(db_id, notion_token, limit=1):
    """
    Fetch Job Description text from Notion database

    Args:
        db_id: Notion database ID
        notion_token: Notion API integration token
        limit: Number of JD entries to fetch (default: 1)

    Returns:
        Combined text from all fetched JD entries
    """
    try:
        notion = Client(auth=notion_token)
        results = notion.databases.query(database_id=db_id, page_size=limit)
        jd_texts = []

        for r in results.get('results', []):
            props = r.get('properties', {})

            # Try different possible field names for JD
            jd_field = props.get('Job Description') or props.get('JD') or props.get('Description')

            if jd_field:
                # Handle rich_text type
                if 'rich_text' in jd_field:
                    jd_texts.append(" ".join([t['plain_text'] for t in jd_field['rich_text']]))
                # Handle title type
                elif 'title' in jd_field:
                    jd_texts.append(" ".join([t['plain_text'] for t in jd_field['title']]))

        combined_text = " ".join(jd_texts)
        if combined_text:
            print(f"✅ Fetched JD from Notion ({len(combined_text)} characters)")
        else:
            print("⚠️  No JD text found in Notion database")

        return combined_text

    except Exception as e:
        print(f"❌ Error fetching from Notion: {e}")
        return ""


def build_cv(group, keywords, jd_text=None):
    """
    Build CV HTML from template

    Args:
        group: CV group identifier (e.g., 'G1_mechanical_project')
        keywords: Comma-separated keywords to highlight
        jd_text: Optional job description text from Notion

    Returns:
        Path to generated CV file
    """
    # Load profile data
    profile = load_profile()

    # Load template
    template_path = TEMPLATES_DIR / f"{group}.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())

    # Render template
    rendered = template.render(
        profile=profile,
        keywords=keywords,
        jd=jd_text,
        group=group
    )

    # Ensure outputs directory exists
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save rendered CV
    safe_name = profile['name'].replace(' ', '_')
    output_filename = f"{safe_name}_{group}.html"
    output_path = OUTPUTS_DIR / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

    print(f"✅ CV generated: {output_path}")
    return str(output_path)


def upload_to_drive(file_path, folder_id=None, credentials_path="credentials.json"):
    """
    Upload file to Google Drive

    Args:
        file_path: Path to file to upload
        folder_id: Optional Google Drive folder ID
        credentials_path: Path to Google Drive credentials file

    Returns:
        Google Drive file ID
    """
    try:
        # Setup authentication
        gauth = GoogleAuth()

        # Try to load saved credentials
        if os.path.exists(credentials_path):
            gauth.LoadCredentialsFile(credentials_path)

        # Authenticate
        if gauth.credentials is None:
            # First time authentication
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh expired credentials
            gauth.Refresh()
        else:
            # Use valid credentials
            gauth.Authorize()

        # Save credentials for next time
        gauth.SaveCredentialsFile(credentials_path)

        # Create Drive instance
        drive = GoogleDrive(gauth)

        # Create file metadata
        file_metadata = {'title': os.path.basename(file_path)}
        if folder_id:
            file_metadata['parents'] = [{'id': folder_id}]

        # Create and upload file
        gfile = drive.CreateFile(file_metadata)
        gfile.SetContentFile(file_path)
        gfile.Upload()

        print(f"✅ Uploaded to Drive: {gfile['title']} (ID: {gfile['id']})")
        return gfile['id']

    except Exception as e:
        print(f"❌ Error uploading to Drive: {e}")
        raise


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='CV Automation MVP - Generate tailored CVs and upload to Google Drive'
    )

    parser.add_argument(
        '--group',
        required=True,
        choices=[
            'G1_mechanical_project',
            'G2_product_manufacturing',
            'G3_hvac_datacenter',
            'G4_automation_systems',
            'G5_innovation_techlead'
        ],
        help='CV group/template to use'
    )

    parser.add_argument(
        '--keywords',
        default='',
        help='Comma-separated keywords to highlight in CV'
    )

    parser.add_argument(
        '--notion-db',
        dest='notion_db',
        default=None,
        help='Notion database ID to fetch JD from'
    )

    parser.add_argument(
        '--notion-token',
        dest='notion_token',
        default=None,
        help='Notion API integration token'
    )

    parser.add_argument(
        '--folder-id',
        dest='folder_id',
        default=None,
        help='Google Drive folder ID to upload to'
    )

    parser.add_argument(
        '--skip-upload',
        action='store_true',
        help='Skip uploading to Google Drive (just generate CV locally)'
    )

    args = parser.parse_args()

    # Fetch JD from Notion if configured
    jd_text = None
    if args.notion_db and args.notion_token:
        print("📝 Fetching Job Description from Notion...")
        jd_text = get_jd_from_notion(args.notion_db, args.notion_token)

    # Generate CV
    print(f"🔨 Building CV for group: {args.group}")
    cv_path = build_cv(args.group, args.keywords, jd_text)

    # Upload to Google Drive
    if not args.skip_upload:
        print("☁️  Uploading to Google Drive...")
        upload_to_drive(cv_path, args.folder_id)
    else:
        print("⏭️  Skipping Google Drive upload")

    print("\n✨ Done!")


if __name__ == "__main__":
    main()
