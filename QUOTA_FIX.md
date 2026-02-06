# Google API Quota Issue - RESOLVED

## Problem Identified

The integration test was failing because the **Google API key has exceeded its quota**. The error was:

```
429 You exceeded your current quota, please check your plan and billing details.
```

## Root Cause

1. Opinions were being submitted successfully (HTTP 201)
2. The state transition triggered the Habermas Machine
3. Habermas Machine called the Google Gemini API
4. The API returned a 429 quota error
5. The error was being logged but **silently swallowed**, so the API returned success even though the transition failed
6. The deliberation remained stuck in the "opinion" stage

## Fixes Applied

### 1. Better Error Handling ✅

Updated `backend/app/api/deliberations.py` to:
- Catch Google API quota errors specifically
- Return HTTP 503 with clear error message
- Include instructions on how to fix it
- Apply to both opinion and critique submissions

### 2. Model Name Update ✅

Updated `backend/app/config.py`:
- Changed from deprecated `gemini-1.5-flash`
- Now using `gemini-flash-latest` (Gemini 2.0/2.5)

### 3. Fixed Habermas Machine Integration ✅

Previously fixed:
- Typo in import: `LLMClient` → `LLMCLient`
- Added environment variable: `os.environ['GOOGLE_API_KEY'] = settings.GOOGLE_API_KEY`

## What You Need to Do

### Get a New Google API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Create a new API key (or use existing one with available quota)
3. Copy the key

### Update Configuration

Edit `backend/.env` and replace the GOOGLE_API_KEY:

```bash
GOOGLE_API_KEY=your_new_api_key_here
```

### Restart Backend

```bash
# Kill the current backend process
# Then restart it
cd backend
uvicorn app.main:app --reload --port 8000
```

### Run Integration Test Again

```bash
python scripts/integration_test.py
```

## Expected Behavior After Fix

1. Submit 3 opinions → all accepted (HTTP 201)
2. Habermas Machine runs (30-60 seconds)
3. State transitions to "ranking"
4. 16 candidate statements generated
5. Test continues through full workflow

## API Key Quota Limits

**Free Tier (Google AI Studio):**
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per day

**If you need more:**
- Upgrade to paid tier
- Or space out test runs to avoid rate limits

## Verification

After getting a new API key, you can verify it works:

```bash
# Test the API key directly
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=YOUR_API_KEY"
```

If this returns JSON with "candidates" field, your key is working!

---

## Next Steps After Fixing

Once you have a new API key and the integration test passes:

1. ✅ Complete integration testing
2. Deploy backend to Railway
3. Deploy frontend to Vercel
4. Test with real OpenClaw agents
5. Document for users

