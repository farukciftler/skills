# ASO Metadata Character Limits & Indexing Rules

## iOS App Store Connect vs Google Play Console Matrix

| Metadata Field | iOS App Store | Google Play Store | Indexed by Algorithm? |
| :--- | :--- | :--- | :--- |
| **App Title** | 30 Characters | 30 Characters | **Yes** (Both platforms - Primary Weighting) |
| **Subtitle / Short Desc.** | 30 Characters | 80 Characters | **Yes** (Both platforms - High Weighting) |
| **Keyword Field** | 100 Bytes (Hidden) | N/A | **Yes** (iOS Only) |
| **Long Description** | 4,000 Characters | 4,000 Characters | **Google Play Only** (Not indexed by iOS) |
| **Promotional Text** | 170 Characters | N/A | **No** (CRO / Marketing Copy) |
| **Developer Name** | Account Name | Account Name | **Yes** (Both platforms) |
| **In-App Purchases** | 30 Char Title | 30 Char Title | **Yes** (Can rank independently in search) |

## iOS Keyword Field Optimization Rules
- Format: `word1,word2,word3,word4`
- Never insert spaces after commas (wastes bytes).
- Do not repeat words used in Title, Subtitle, Category name, or Publisher name.
- Use singular forms (Apple algorithm handles basic plurals).
- Combine words dynamically: if Title has "Fitness" and Keyword field has "Tracker", iOS will index "Fitness Tracker".
