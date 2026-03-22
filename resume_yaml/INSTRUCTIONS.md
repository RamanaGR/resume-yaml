# Resume YAML — Instructions

Place your resume YAML files in this folder (`resume_yaml/`). Use `sample_resume.yaml` as a template.

Required top-level keys:
- `cv`: contact and metadata (name, title, location, email, phone)
- `sections`: grouped content such as `experience`, `education`, `skills`, and `projects`

Quickstart

```bash
# Generate PDF from a sample YAML
python3 main.py resume_yaml/sample_resume.yaml Sample_Resume.pdf
```

Notes
- Keep personal or sensitive files out of the repository; they are ignored by `.gitignore`.
- If you need to add a new resume YAML, copy `sample_resume.yaml` and edit the fields.
