# Google Sheets Webhook Setup (For Cloud Data Saving)

Since Google Sheets doesn't allow direct writes from public clients, we need to create a simple webhook using **Google Apps Script**. This takes 10 minutes but requires no secrets in your app.

## Part 1: Create the Google Apps Script Webhook (10 minutes)

### Step 1: Open Your Google Sheet
1. Open your sheet: `https://docs.google.com/spreadsheets/d/1zvVYeJs3rTMhRmeh-AxPSe6SAFGaXELYkVyhSwSMoho/edit`
2. Click **Extensions** → **Apps Script**

### Step 2: Create the Webhook Script
1. Delete any existing code in the editor
2. Paste this code:

```javascript
function doPost(e) {
  try {
    // Get the active spreadsheet
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
    
    // Parse the incoming JSON data
    var data = JSON.parse(e.postData.contents);
    
    // Get the next user ID
    var lastRow = sheet.getLastRow();
    var userId = lastRow; // Header is row 1, so this gives the next ID
    
    // Prepare the row data
    var rowData = [
      userId,
      data.timestamp,
      data.name,
      data.email,
      data.age_category,
      data.sex,
      data.bmi,
      data.high_bp,
      data.high_chol,
      data.smoker,
      data.diabetes_risk,
      data.risk_percentage,
      data.prediction
    ];
    
    // Append the row
    sheet.appendRow(rowData);
    
    // Return success
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'success',
      'user_id': userId
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch(error) {
    // Return error
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'error',
      'message': error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function (optional)
function testPost() {
  var testData = {
    postData: {
      contents: JSON.stringify({
        timestamp: '2025-11-24 12:00:00',
        name: 'Test User',
        email: 'test@example.com',
        age_category: 5,
        sex: 1,
        bmi: 25.5,
        high_bp: 0,
        high_chol: 0,
        smoker: 0,
        diabetes_risk: 'Low Risk',
        risk_percentage: 15.5,
        prediction: 0
      })
    }
  };
  
  var result = doPost(testData);
  Logger.log(result.getContent());
}
```

### Step 3: Deploy as Web App
1. Click the **Deploy** button (top right) → **New deployment**
2. Click the gear icon ⚙️ next to "Select type"
3. Choose **Web app**
4. Fill in:
   - **Description**: "Diabetes Assessment Webhook"
   - **Execute as**: **Me**
   - **Who has access**: **Anyone** (this is important!)
5. Click **Deploy**
6. Click **Authorize access**
7. Choose your Google account
8. Click **Advanced** → **Go to [your project]** (if warning appears)
9. Click **Allow**

### Step 4: Copy the Webhook URL
1. After deployment, you'll see a **Web app URL** like:
   ```
   https://script.google.com/macros/s/AKfycbz.../exec
   ```
2. **Copy this entire URL** - you'll need it in the next part!

## Part 2: Update Your App Code (2 minutes)

### Step 1: Update database.py
1. Open `health-risk-assessment/src/utils/database.py`
2. Find line ~32 where it says:
   ```python
   GOOGLE_SHEET_ID = "1zvVYeJs3rTMhRmeh-AxPSe6SAFGaXELYkVyhSwSMoho"
   ```

3. Add a new line right after it with your webhook URL:
   ```python
   GOOGLE_SHEET_ID = "1zvVYeJs3rTMhRmeh-AxPSe6SAFGaXELYkVyhSwSMoho"
   GOOGLE_APPS_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_ACTUAL_URL_HERE/exec"
   ```

### Step 2: Commit and Push
```bash
git add health-risk-assessment/src/utils/database.py
git commit -m "Add Google Apps Script webhook URL"
git push
```

## Testing

1. Go to your deployed app
2. Complete an assessment
3. Check your Google Sheet - the data should appear!

## Troubleshooting

### "Authorization required" error:
- Make sure you set "Who has access" to **Anyone**
- Redeploy the script if you changed settings

### Data not appearing:
- Check the Apps Script execution logs: Apps Script editor → **Executions** (left sidebar)
- Verify the webhook URL is correct
- Make sure the sheet tab is named "Sheet1" (or update the script)

### "Script function not found":
- Make sure you clicked **Deploy** not just **Save**
- The URL should end with `/exec` not `/dev`

## How It Works

1. Your Streamlit app sends HTTP POST requests to the Google Apps Script webhook
2. The webhook has permission to write to your Google Sheet (because it runs as you)
3. The webhook appends new rows to your sheet
4. No authentication needed in your Streamlit app!

## Security Note

- The webhook URL is public, but it only allows appending data to your sheet
- Anyone with the URL can add data, but cannot read or modify existing data
- For production apps with sensitive data, implement authentication in the Apps Script
- For portfolio/demo projects, this setup is fine

## Alternative: Disable Cloud Saving

If you don't want to set up the webhook, you can simply leave it disabled:
- The app will work perfectly without saving
- All features (risk assessment, PDF reports, recommendations) still function
- Only the historical data tracking won't work in the cloud deployment
