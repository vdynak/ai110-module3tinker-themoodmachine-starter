"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "healed",
    "fire",
    "sick",
    "wicked",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "annoyed",
    "exhausted",
    "stuck",
    "missing",
    "died",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "That concert was actually amazing 😂",
    "lowkey annoyed that my package is still missing",
    "I passed the quiz but now I'm stressed about the project 😅",
    "meh, it's just another Monday",
    "No cap, that meal healed my soul",
    "I absolutely love waiting 40 minutes for the bus",
    "kinda want to go out, kinda want to hide under a blanket 🥲",
    "sure, everything is totally under control lol",
    "I'm not mad, just disappointed tbh",
    "Finals are brutal but I'm weirdly motivated",
    "Best nap ever, I'm reborn 😂",
    "lol everything is on fire but we're chilling",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  # "That concert was actually amazing 😂"
    "negative",  # "lowkey annoyed that my package is still missing"
    "mixed",     # "I passed the quiz but now I'm stressed about the project 😅"
    "neutral",   # "meh, it's just another Monday"
    "positive",  # "No cap, that meal healed my soul"
    "negative",  # "I absolutely love waiting 40 minutes for the bus"
    "mixed",     # "kinda want to go out, kinda want to hide under a blanket 🥲"
    "negative",  # "sure, everything is totally under control lol"
    "negative",  # "I'm not mad, just disappointed tbh"
    "mixed",     # "Finals are brutal but I'm weirdly motivated"
    "positive",  # "Best nap ever, I'm reborn 😂"
    "mixed",     # "lol everything is on fire but we're chilling"
]

# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
