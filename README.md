# kiro-cli-jenkins-build-triage

AI-powered build failure triage using Kiro CLI headless mode in a Jenkins pipeline. Uses a minimal Strands weather agent as the sample application.

## The Demo

The app is intentionally simple — a Strands agent with one tool. The point is the **Jenkinsfile**: when a build fails, Jenkins pipes the build log and git diff into `kiro-cli --headless`, which returns a root cause analysis and suggested fix.

## Project Structure

```
agent.py          — Strands weather agent (11 lines)
tools.py          — Weather lookup tool using wttr.in
test_tools.py     — Unit tests
Dockerfile        — Container image
Jenkinsfile       — Pipeline with Kiro headless triage on failure
requirements.txt  — Dependencies
```

## Try It Locally

```bash
pip install -r requirements.txt
pytest test_tools.py -v
python agent.py
```

## Demo the Failure Triage

1. Break something in `tools.py` (e.g., change `temp_F` to `temp_X`)
2. Commit and push
3. Jenkins build fails at the Test stage
4. `post { failure {} }` triggers Kiro headless
5. Kiro analyzes the test log + your diff and identifies the root cause
