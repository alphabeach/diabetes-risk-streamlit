# One-Time Google Sheets Setup (5 Minutes, No Secrets!)

Enable data saving in your deployed app with this **simple 5-step setup**. No API keys, no service accounts, no complicated configuration!

## Quick Setup

### Step 1: Create a Google Sheet (2 minutes)

1. Go to [Google Sheets](https://sheets.google.com/)
2. Click **"+ Blank"** to create a new spreadsheet
3. Name it: `Diabetes Assessments`
4. Add header row - Paste this into cells A1 through M1:

```
user_id	timestamp	name	email	age_category	sex	bmi	high_bp	high_chol	smoker	diabetes_risk	risk_percentage	prediction
```

Or copy these one by one:
- A1: `user_id`
- B1: `timestamp`
- C1: `name`
- D1: `email`
- E1: `age_category`
- F1: `sex`
- G1: `bmi`
- H1: `high_bp`
- I1: `high_chol`
- J1: `smoker`
- K1: `diabetes_risk`
- L1: `risk_percentage`
- M1: `prediction`

### Step 2: Make it Publicly Writable (30 seconds)

1. Click the **"Share"** button (top right corner)
2. Click **"Change to anyone with the link"**
3. In the dropdown next to "Viewer", select **"Editor"**
4. Click **"Done"**

⚠️ **Security Note**: This allows anyone with the link to edit. Perfect for portfolio projects. For production with sensitive data, use proper authentication.

### Step 3: Get the Sheet ID (30 seconds)

1. Look at your Google Sheet URL in the browser:
   ```
   https://docs.google.com/spreadsheets/d/1ABC123XYZ456789DEFGH/edit#gid=0
   ```

2. Copy everything between `/d/` and `/edit`
   
   In this example: `1ABC123XYZ456789DEFGH`

### Step 4: Update the Code (1 minute)

1. Open `health-risk-assessment/src/utils/database.py` in your editor

2. Find line 29 (or search for `GOOGLE_SHEET_ID`):
   ```python
   GOOGLE_SHEET_ID = None  # Example: "1ABC123XYZ789-yourSheetId"
   ```

3. Replace `None` with your Sheet ID in quotes:
   ```python
   GOOGLE_SHEET_ID = "1ABC123XYZ456789DEFGH"  # Your actual Sheet ID
   ```

4. Save the file

### Step 5: Deploy (1 minute)

```bash
git add health-risk-assessment/src/utils/database.py
git commit -m "Configure Google Sheet for data storage"
git push
```

**Done!** 🎉 Streamlit Cloud will auto-redeploy and start saving data to your Google Sheet.

---

## Viewing Your Data

### Real-time Access:
- Open your Google Sheet anytime to see all assessments
- Data appears instantly after each assessment
- No need to download or export

### Export Options:
- **Excel**: File → Download → Microsoft Excel (.xlsx)
- **CSV**: File → Download → Comma Separated Values (.csv)
- **PDF**: File → Download → PDF Document (.pdf)

### Analysis:
- Create charts directly in Google Sheets
- Use pivot tables
- Apply formulas for custom metrics
- Share with team members

---

## How It Works

### Technical Details:

**In Cloud (Streamlit):**
- Uses Google Sheets public API
- Appends data via HTTP POST requests
- Reads data via CSV export endpoint
- **No authentication required** for public sheets
- Works immediately with just the Sheet ID

**Locally (Your Computer):**
- Saves to `data/assessment_history.csv`
- No Google Sheets needed
- Works offline

### API Calls:
- **Write**: `POST /values/Sheet1!A:M:append`
- **Read**: `GET /export?format=csv`
- Both work on publicly writable sheets without API keys

---

## Troubleshooting

### "Permission denied" when trying to save:
✅ **Fix**: Make sure the Google Sheet is set to **"Anyone with the link can edit"** (not just "View")

1. Click Share button
2. Check that it says "Anyone with the link"
3. Check that the dropdown says "Editor"

### Data not appearing in the sheet:
✅ **Fix**: Verify the Sheet ID is correct

1. Double-check you copied the entire ID from the URL
2. Make sure the ID is in quotes in the code
3. Check Streamlit Cloud logs for errors

### Header row issues:
✅ **Fix**: Ensure you have exactly 13 columns with the correct names

```
user_id, timestamp, name, email, age_category, sex, bmi, high_bp, high_chol, smoker, diabetes_risk, risk_percentage, prediction
```

### App says "Cloud storage not configured":
✅ **Fix**: Check that `GOOGLE_SHEET_ID` is set in the code

1. Open `src/utils/database.py`
2. Line 29 should have: `GOOGLE_SHEET_ID = "your-id-here"`
3. Make sure you committed and pushed the changes

### Want to disable cloud saving?:
✅ **Fix**: Set the Sheet ID back to `None`

```python
GOOGLE_SHEET_ID = None
```

---

## Security Considerations

### For Personal/Portfolio Projects (Current Setup):
✅ **Pros**:
- Simple setup
- No authentication needed
- Perfect for demos
- Easy to share results

⚠️ **Limitations**:
- Anyone with the Sheet link can view/edit data
- Not suitable for sensitive health information
- Best for demonstration purposes

### For Production Apps:
Consider using:
- Google Sheets API with service accounts
- Proper database (PostgreSQL, MongoDB)
- Authentication and encryption
- HIPAA-compliant storage for health data

---

## Questions?

**Can multiple people use the app at once?**  
Yes! Google Sheets handles concurrent writes automatically.

**Is there a limit to how much data I can store?**  
Google Sheets supports up to 5 million cells. At 13 columns per assessment, that's ~384,000 assessments.

**Can I use a different sheet name?**  
Yes, but you'll need to update the code to reference the correct sheet name.

**What if I want to keep data private?**  
Follow Google's documentation for service account authentication, or use a proper database.

---

## What's Next?

After setup, your deployed app will:
- ✅ Save every assessment to Google Sheets
- ✅ Show statistics in the Quick Stats sidebar
- ✅ Display data in the Admin Dashboard
- ✅ Allow export/analysis of all assessments

Check your Google Sheet after completing a few assessments to see the data flowing in!
