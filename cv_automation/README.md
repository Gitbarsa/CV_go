# CV Automation MVP (v1)

Auto-generate tailored CVs for different job profiles and upload them to Google Drive, with optional Job Description fetching from Notion.

## Features

- **5 Tailored CV Templates**: Each optimized for specific roles:
  - G1: Mechanical Project Engineer
  - G2: Product & Manufacturing Engineer
  - G3: HVAC & Data Center Engineer
  - G4: Automation Systems Engineer
  - G5: Innovation & Tech Lead

- **Notion Integration**: Automatically fetch Job Descriptions from your Notion database to seed keyword matching

- **Google Drive Upload**: Seamlessly upload generated CVs to your Google Drive folder

- **Jinja2 Templating**: Flexible, maintainable HTML templates with dynamic content

## Project Structure

```
cv_automation/
├── templates/              # HTML templates for each CV group
│   ├── G1_mechanical_project.html
│   ├── G2_product_manufacturing.html
│   ├── G3_hvac_datacenter.html
│   ├── G4_automation_systems.html
│   └── G5_innovation_techlead.html
├── data/
│   └── profile.json       # Your professional profile data
├── outputs/               # Generated CVs (created automatically)
├── build.py              # Main automation script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup

### 1. Install Dependencies

```bash
cd cv_automation
pip install -r requirements.txt
```

### 2. Configure Profile Data

Edit `data/profile.json` with your professional information:

```json
{
  "name": "Your Name",
  "title": "Your Professional Title",
  "email": "your.email@example.com",
  "phone": "+1 (555) 123-4567",
  "linkedin": "linkedin.com/in/yourprofile",
  "location": "City, State",
  "summary": "Your professional summary...",
  "skills": [...],
  "experience": [...],
  "education": [...],
  "certifications": [...],
  "projects": {
    "G1_mechanical": [...],
    "G2_manufacturing": [...],
    "G3_hvac": [...],
    "G4_automation": [...],
    "G5_innovation": [...]
  }
}
```

### 3. Google Drive Setup (Optional)

To enable Google Drive uploads:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials
5. Download the credentials as `credentials.json` and place it in the `cv_automation/` directory
6. On first run, you'll be prompted to authorize access via browser

### 4. Notion Setup (Optional)

To enable Job Description fetching from Notion:

1. Create a [Notion Integration](https://www.notion.so/my-integrations)
2. Get your integration token (starts with `secret_`)
3. Share your database with the integration
4. Get your database ID from the database URL:
   ```
   https://notion.so/<workspace>/<database_id>?v=...
                              ↑
                      This is your database ID
   ```

## Usage

### Basic Usage (Local Generation Only)

Generate a CV without uploading to Drive:

```bash
python build.py \
  --group G3_hvac_datacenter \
  --keywords "HVAC, Data Center, Commissioning" \
  --skip-upload
```

### With Google Drive Upload

Generate and upload to Google Drive:

```bash
python build.py \
  --group G1_mechanical_project \
  --keywords "Project Management, CAD, Mechanical Design" \
  --folder-id YOUR_GDRIVE_FOLDER_ID
```

### With Notion Integration

Fetch JD from Notion and include it in the CV:

```bash
python build.py \
  --group G4_automation_systems \
  --keywords "PLC, SCADA, Automation" \
  --notion-db YOUR_NOTION_DATABASE_ID \
  --notion-token secret_YOUR_NOTION_TOKEN \
  --folder-id YOUR_GDRIVE_FOLDER_ID
```

### Full Example (All Features)

```bash
python build.py \
  --group G5_innovation_techlead \
  --keywords "Innovation, Leadership, R&D, Technology Strategy" \
  --notion-db abc123def456 \
  --notion-token secret_xyz789 \
  --folder-id 1AbCdEfGhIjKlMnOpQrStUvWxYz
```

## Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--group` | Yes | CV group/template to use (G1-G5) |
| `--keywords` | No | Comma-separated keywords to highlight |
| `--notion-db` | No | Notion database ID for JD fetching |
| `--notion-token` | No | Notion API integration token |
| `--folder-id` | No | Google Drive folder ID for upload |
| `--skip-upload` | No | Skip Google Drive upload (local only) |

## Available CV Groups

| Group ID | Focus Area | Best For |
|----------|------------|----------|
| `G1_mechanical_project` | Mechanical Engineering & Project Management | Project-focused mechanical roles |
| `G2_product_manufacturing` | Product Development & Manufacturing | Manufacturing and production roles |
| `G3_hvac_datacenter` | HVAC Systems & Data Center Infrastructure | HVAC, commissioning, data center roles |
| `G4_automation_systems` | Automation, Controls & SCADA | Automation and control systems roles |
| `G5_innovation_techlead` | Innovation Leadership & R&D | Leadership, innovation, executive roles |

## Output

Generated CVs are saved to the `outputs/` directory with the naming convention:

```
{YourName}_{group_id}.html
```

For example: `JohnDoe_G3_hvac_datacenter.html`

## Troubleshooting

### Google Drive Authentication Issues

If you encounter authentication errors:

1. Delete the `credentials.json` file
2. Re-download credentials from Google Cloud Console
3. Ensure the Google Drive API is enabled
4. Try authenticating again

### Notion API Errors

Common issues:

- **404 Not Found**: Check that your database ID is correct
- **401 Unauthorized**: Verify your integration token
- **403 Forbidden**: Ensure the database is shared with your integration

### Template Errors

If templates aren't rendering correctly:

1. Verify `profile.json` has all required fields
2. Check that the template file exists in `templates/`
3. Ensure Jinja2 syntax is correct in templates

## Customization

### Modifying Templates

Edit the HTML files in `templates/` to customize the CV design. Each template uses Jinja2 syntax:

```html
<!-- Access profile data -->
<h1>{{ profile.name }}</h1>

<!-- Conditional rendering -->
{% if keywords %}
  <p>Keywords: {{ keywords }}</p>
{% endif %}

<!-- Loops -->
{% for job in profile.experience %}
  <div>{{ job.company }}</div>
{% endfor %}
```

### Adding New CV Groups

1. Create a new HTML template in `templates/`
2. Add corresponding project data in `profile.json`
3. Update the `--group` choices in `build.py`

## Best Practices

1. **Keep profile.json updated**: Regularly update your achievements and projects
2. **Use specific keywords**: Tailor keywords to each job application
3. **Leverage Notion**: Store JDs in Notion for easy reference and automation
4. **Organize Drive folders**: Create separate folders for different job types
5. **Version control**: Keep your templates and profile data in git

## Future Enhancements

- [ ] PDF generation support
- [ ] ATS optimization scoring
- [ ] Keyword density analysis
- [ ] Multi-language support
- [ ] Email delivery integration
- [ ] Template preview in browser

## License

MIT License - feel free to customize and use for your own job search!

## Support

For issues or questions, please refer to the project documentation or open an issue in the repository.

---

**Good luck with your job search!** 🚀
