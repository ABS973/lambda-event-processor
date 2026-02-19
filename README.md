# PL202 – Serverless Event Handler

A Lambda-style serverless event processor that validates, normalizes, and routes cloud events — simulating real AWS Lambda behavior locally.

## Supported Event Types

| Event Type    | Description                        |
|---------------|------------------------------------|
| `USER_SIGNUP` | Validates and normalizes new users |
| `PAYMENT`     | Processes payments with fee calc   |
| `FILE_UPLOAD` | Routes uploads to storage classes  |

## Project Structure

```
├── handler.py          # Core Lambda handler logic
├── run_local.py        # Local test runner
├── run_proof.txt       # Sample output from all test events
├── events/             # Test event JSON files (valid + invalid)
└── expected_outputs/   # Expected outputs for valid events
```

## How to Run

```bash
# Run a single event
python run_local.py --event events/01_user_signup_valid.json

# Run all events
python run_local.py --all
```

## Response Format

Every response follows this structure:

```json
{
  "status": "ok | error",
  "message": "short explanation",
  "data": { "..." },
  "errors": []
}
```

## Validation Rules

- **USER_SIGNUP** — valid email, plan must be `free`, `pro`, or `edu`
- **PAYMENT** — amount must be `> 0`, currency must be `BHD`, `USD`, or `EUR`
- **FILE_UPLOAD** — valid uploader email, `size_bytes >= 0`

## Storage Class Logic

| File Size      | Storage Class |
|----------------|---------------|
| < 1 MB         | `STANDARD`    |
| 1 MB – 50 MB   | `STANDARD_IA` |
| 50 MB+         | `GLACIER`     |

## Course Info

**Course:** PL202 – Cloud Computing  
**Task:** Day 1 – Serverless Event Processing
