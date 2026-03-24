# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Both models were built and compared. The primary model is rule based (`mood_analyzer.py`). The ML model (`ml_experiments.py`) was used as a comparison.

**Intended purpose:**  
Classify short social-media-style text messages (posts, messages, captions) into one of four mood labels: `positive`, `negative`, `neutral`, or `mixed`.

**How it works (brief):**  
The rule based model preprocesses raw text into lowercase tokens, looks up each token against a positive and negative word list, accumulates a numeric score, and maps that score to a label. Negation phrases like "not happy" flip the polarity of the next mood word. The ML model converts each post into a bag-of-words vector using `CountVectorizer` and fits a `LogisticRegression` classifier on those vectors and the human-assigned labels from `TRUE_LABELS`.



## 2. Data

**Dataset description:**  
`SAMPLE_POSTS` contains 18 labeled short posts. The starter dataset had 6 posts. We added 12 new posts in two rounds. The first round added examples covering slang, emojis, sarcasm, and mixed emotions. The second round added 4 more posts to test model sensitivity to dataset changes.

**Labeling process:**  
Each post was labeled manually using four categories:
- `positive` for generally uplifting or happy tone
- `negative` for frustration, sadness, or sarcasm aimed at a bad situation
- `neutral` for flat, factual, or ambiguous posts with no clear mood signal
- `mixed` for posts that contain both positive and negative feelings in the same sentence

Hard-to-label examples included:
- "This is fine" — could be neutral resignation (frustration disguised as neutrality) or genuinely neutral
- "kinda want to go out, kinda want to hide under a blanket 🥲" — mixed, but the ambivalence is subtle
- "sure, everything is totally under control lol" — labeled negative because of implied sarcasm; another person might read it as neutral

**Important characteristics of your dataset:**  
- Contains informal slang: "lowkey", "no cap", "tbh", "lol"
- Includes emojis as tone signals: 😂, 😅, 🥲
- Includes sarcastic posts where the literal words contradict the intended meaning
- Contains posts with genuinely mixed emotions in the same sentence
- Posts are all short (under 15 words), similar to real social media messages

**Possible issues with the dataset:**  
- Small size: 18 examples is not enough for reliable generalization
- Label imbalance: negative (6), positive (5), mixed (4), neutral (3)
- Sarcasm is labeled by human inference; another labeler might disagree
- The same word can shift meaning by context ("fire" as slang vs. literal fire)

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Preprocessing (`preprocess` in `mood_analyzer.py`):
- Strips whitespace and lowercases the text
- Uses a regex tokenizer that extracts words, contractions (e.g., `i'm`, `it's`), emoticons, and emoji characters as separate tokens
- Drops standalone punctuation like commas and periods that carry no mood signal

Scoring (`score_text`):
- Starts at 0
- For each token, adds +1 if it matches a word in `POSITIVE_WORDS`, subtracts 1 for `NEGATIVE_WORDS`
- Negation detection: if a token is in `{"not", "never", "no"}` and the next token is a mood word, the polarity is flipped rather than adding. For example, "not happy" applies -1 instead of +1, and "not bad" applies +1 instead of -1.

Label mapping (`predict_label`):
- If both positive and negative tokens appear and `abs(score) <= 1`, returns `mixed`
- If `score > 0`, returns `positive`
- If `score < 0`, returns `negative`
- Otherwise returns `neutral`

Vocabulary enhancements (in `dataset.py`):
- Expanded `POSITIVE_WORDS` with: `hopeful`, `proud`, `healed`, `fire`, `sick`, `wicked`
- Expanded `NEGATIVE_WORDS` with: `annoyed`, `exhausted`, `stuck`, `missing`, `died`

**Strengths of this approach:**  
- Fully transparent: every decision can be traced to a specific token and rule
- Fast and requires no training data
- Negation handling correctly flips polarity for common patterns like "not happy" and "not bad"
- Adding a word to a list immediately changes behavior, making targeted fixes easy

**Weaknesses of this approach:**  
- Sarcasm is not detectable: "I absolutely love waiting 40 minutes for the bus" matches `love` and returns `positive`
- Slang and context-dependent words are problems: `sick` was added as positive slang, but the same word in a medical context would be negative
- One strong token can dominate the score even when the rest of the sentence contradicts it
- Emojis are tokenized but not scored because they are not in the word lists
- Mixed tone is only detected when both a positive and negative word appear; subtle mixed tone with no lexicon hits is flattened to `neutral`

## 4. How the ML Model Works (if used)

**Features used:**  
Bag-of-words representation using scikit-learn's `CountVectorizer`. Each post becomes a vector where each dimension counts how many times a vocabulary word appears. No preprocessing from `mood_analyzer.py` is used; the vectorizer tokenizes independently.

**Training data:**  
Trained on `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py` (18 labeled examples).

**Training behavior:**  
The ML model always reports 1.00 accuracy on its evaluation because it trains and evaluates on the same dataset (no train/test split). When the dataset was expanded from 14 to 18 posts, the model immediately absorbed the new labels and maintained 1.00 on training data. This is memorization, not generalization. On the 8 unseen "breaker" sentences tested outside the training set, the ML model frequently predicted `negative` for inputs with few or no training vocabulary matches, because the class with the highest prior and intercept bias dominated when information was sparse.

**Strengths and weaknesses:**  
Strengths:
- Learns patterns directly from labeled data without requiring hand-written rules
- Automatically adapts when new labeled examples are added
- Can implicitly learn word co-occurrence patterns that rules miss

Weaknesses:
- With 18 examples it memorizes the training set rather than learning general patterns
- No train/test split means the 1.00 reported accuracy is misleading
- Unseen tokens contribute nothing; vocabulary coverage is limited to the training set
- Class imbalance in the small dataset biases predictions toward the majority class on ambiguous inputs

## 5. Evaluation

**How you evaluated the model:**  
Both models were evaluated against `TRUE_LABELS` on the full `SAMPLE_POSTS` dataset using the `evaluate_rule_based` function in `main.py` and the `evaluate_on_dataset` function in `ml_experiments.py`. Accuracy is computed as the fraction of predictions that exactly match the true label.

Rule based model final accuracy: **0.56** (10/18 correct)  
ML model accuracy on training data: **1.00** (18/18, same as training set — not a reliable measure)

**Examples of correct predictions:**

1. "I love this class so much" → `positive`  
   The token `love` is in `POSITIVE_WORDS`. No negation. Score = 1. Clear, unambiguous, and both models agree.

2. "lowkey annoyed that my package is still missing" → `negative`  
   After vocabulary expansion, `annoyed` and `missing` both score -1. Score = -2. This was a previous failure that the targeted vocabulary fix resolved.

3. "Feeling tired but kind of hopeful" → `mixed`  
   `tired` scores -1 and `hopeful` was added to `POSITIVE_WORDS`. Score = 0 with both signals present, so `mixed` is returned. Previously wrong before the vocab update.

**Examples of incorrect predictions:**

1. "I absolutely love waiting 40 minutes for the bus" — predicted `positive`, true `negative`  
   The token `love` scores +1. No other lexicon words appear. The model sees a positive word and nothing else. It cannot infer that "waiting 40 minutes for the bus" is a frustrating situation. This is a fundamental sarcasm failure.

2. "Best nap ever, I'm reborn 😂" — predicted `neutral`, true `positive`  
   The rule model has no matches: `best`, `nap`, `ever`, `reborn` are all outside the lexicon. The emoji `😂` is tokenized but not scored. Score = 0 with no positive or negative hits → `neutral`.

3. "sure, everything is totally under control lol" — predicted `neutral`, true `negative`  
   No lexicon words match. `lol` and `sure` are not scored. The sarcastic tone comes from implied context, which rule-based scoring cannot read. ML correctly predicts `negative` here because it learned from a training example with similar structure.

## 6. Limitations

- **Small dataset:** 18 examples is far too few for reliable generalization. Both models are heavily shaped by individual labeling choices.
- **Sarcasm is undetectable by rules:** Any sentence where the surface words are positive but the intent is negative will confuse the rule-based model. There is no rule that can reliably distinguish "I love this class" from "I absolutely love waiting 40 minutes for the bus" without external context.
- **Emoji blindness in rule model:** Emojis like 😂, 🥲, and 😅 are tokenized correctly but contribute 0 to the score. They carry clear tone information that is wasted.
- **Ambiguous slang:** Words added to handle one use case can damage another. "Sick" was added as positive slang but would be misread as positive in "I've been sick all week."
- **ML accuracy is inflated:** The ML model is trained and evaluated on the same 18 examples. The 1.00 figure is not a measure of real performance. Tested on unseen sentences, it tends to predict `negative` when vocabulary is sparse.
- **No handling of intensifiers or diminishers:** "A little sad" and "devastated" score the same (-1). "So happy" and "okay I guess" both score 0 or 1.
- **Mixed class is hard to trigger:** The mixed label only fires when both positive and negative lexicon words appear. Mixed-emotion sentences that use out-of-vocabulary words (e.g., "Finals are brutal but I'm weirdly motivated") fall through to `neutral`.

## 7. Ethical Considerations

- **Misclassifying distress:** A post expressing genuine sadness or crisis ("I can't do this anymore") could be misclassified as `neutral` if the words fall outside the lexicon. In a real application, a wrong label could mean missing a person who needs support.
- **Cultural and community language bias:** The vocabulary and examples reflect one dialect and cultural context (primarily English-language internet slang). Words, emoji use, and tone norms vary across communities. A model trained on this narrow dataset would be less accurate for people whose language patterns are not represented.
- **Sarcasm misclassification has unequal effects:** Sarcasm is used differently across cultures, ages, and communities. A model that systematically misreads sarcasm as positive is not a neutral error — it may disproportionately misread the tone of specific groups.
- **Privacy:** If this system were deployed to analyze personal messages or posts, users should be made aware that their text is being processed. Mood inference from private text raises consent concerns even at the prototype stage.
- **Label subjectivity:** Human mood labels are not ground truth. Two people may disagree on whether a post is `mixed` or `negative`. Systems trained on subjective labels embed those assumptions invisibly.

## 8. Ideas for Improvement

- **Add more labeled data:** The clearest path to better ML performance. Even 100 diverse examples would reduce memorization and expose the model to more language patterns.
- **Create a real held-out test set:** Split `SAMPLE_POSTS` into training and test subsets, or add a separate `TEST_POSTS` / `TEST_LABELS` list so accuracy measurements reflect real generalization.
- **Score emojis explicitly:** Map common emojis to polarity weights in `mood_analyzer.py` (e.g., 🥲 → -0.5, 😂 → +0.5) so they contribute to the score rather than being ignored.
- **Add intensifier and diminisher handling:** Detect words like "so", "super", "absolutely", "a bit", "kind of" and scale the next mood word's contribution accordingly.
- **Use TF-IDF instead of CountVectorizer:** Would give less weight to common words and more weight to distinctive signals; often improves text classification on small datasets.
- **Improve mixed detection:** Currently mixed only fires when both lexicon word types are present. A threshold-based approach (e.g., positive score ≥ 1 and negative score ≤ -1) would capture more nuanced cases.
- **Sarcasm heuristic:** A simple rule like "positive word followed within 5 tokens by a clearly negative situation word" could catch the most common sarcasm patterns (e.g., "love waiting", "great, my phone died").
- **Use a small pre-trained model:** A sentence-transformer or a fine-tuned BERT-tiny model could capture contextual meaning that neither bag-of-words nor keyword rules can access, even with limited training data.
