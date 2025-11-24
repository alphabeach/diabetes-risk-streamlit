# One-Time Google Sheets Setup (No Secrets Needed!)

This is a **5-minute setup** to enable data saving in your deployed app. No API keys, no service accounts, no complicated configuration!

## Step 1: Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Click **"+ Blank"** to create a new spreadsheet
3. Name it: `Diabetes Assessments`
4. In cell A1, add this header row (copy-paste):
   ```
   user_id	timestamp	name	email	age_category	sex	bmi	high_bp	high_chol	smoker	diabetes_risk	risk_percentage	prediction
   ```

## Step 2: Make it Publicly Writable

1. Click the **"Share"** button (top right)
2. Click **"Change to anyone with the link"**
3. In the dropdown, select **"Editor"** (not Viewer!)
4. Click **"Done"**

⚠️ **Security Note**: This allows anyone with the link to write data. For a personal project/portfolio, this is fine. For production apps with sensitive data, you'd want proper authentication.

## Step 3: Get the Sheet ID

1. Look at your Google Sheet URL. It looks like:
   ```
   https://docs.google.com/spreadsheets/d/1ABC123XYZ789/edit#gid=0
   ```

2. Copy the part between `/d/` and `/edit` - that's your Sheet ID
   In the example above: `1ABC123XYZ789`

## Step 4: Update Your Code

1. Open `health-risk-assessment/src/utils/database.py`
2. Find line 19 (around there) that says:
   ```python
   GOOGLE_SHEET_ID = None  # Set this to your Google Sheet ID
   ```

3. Replace it with your Sheet ID:
   ```python
   GOOGLE_SHEET_ID = "1ABC123XYZ789"  # Your actual Sheet ID
   ```

4. Save the file

## Step 5: Commit and Push

```bash
git add health-risk-assessment/src/utils/database.py
git commit -m "Configure Google Sheet for cloud data storage"
git push
```

That's it! Your deployed app will now save assessment data to Google Sheets automatically.

## Viewing Your Data

- Open your Google Sheet anytime to see all saved assessments
- Export to Excel: File → Download → Microsoft Excel
- Create charts and analyze directly in Google Sheets
- Share with others by sending them the Sheet link

## How It Works

### In Cloud (Streamlit):
✅ Saves to your Google Sheet via simple API calls  
✅ No secrets or authentication needed  
✅ Works immediately after setup  

### Locally (Your Computer):
✅ Still saves to `data/assessment_history.csv`  
✅ No Google Sheets needed for local development  

## Troubleshooting

**"Permission denied" when saving:**
- Make sure the sheet is set to "Anyone with the link can **edit**" (not just view)
- Check that the Sheet ID is correct

**Data not appearing:**
- Verify the header row matches exactly (13 columns)
- Check Streamlit Cloud logs for errors

**Want to disable saving again?**
- Set `GOOGLE_SHEET_ID = None` in the code
