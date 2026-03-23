# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

--- "Go Higher" for all the numbers [0, 50, 77, 99] "labels were wrong"
--- Attempt Allowed: 8 (in the instructions) vs Attempt Allowed: 7 (in the app)
--- The submit button needed to be clicked specifically to submit the guess, but the instructions said "press enter" to submit the guess.


## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
--- I used Claude Code Chat to ask about  this project.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
--- Claude Code accurately suggested the fix to the check_guess function and ensured it was generating the correct labels for the hints.
AI suggested the following - 
```python
# Before (wrong):
if guess > secret:
    return "Too High", "📈 Go HIGHER!"
else:
    return "Too Low", "📉 Go LOWER!"

# After (correct):
if guess > secret:
    return "Too High", "📉 Go LOWER!"
else:
    return "Too Low", "📈 Go HIGHER!"
```
I verified the above by running the game and matching the logic of the game myself.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
--- The "Enter your guess and press enter to submit" instruction was misleading because the app required clicking the "Submit Guess" button to submit the guess, rather than pressing the Enter key. I wanted to fix this so that the guess would be submitted if I pressed the "Enter" key. However, Claude Code's suggestion did not actually fix the problem.
AI suggested the following to fix the issue:
``The issue is that st.text_input reruns the app when Enter is pressed, but the submit logic only runs when if submit: (the button click) is True. The fix is to wrap the input and submit button in a st.form, which makes pressing Enter trigger the form submission.

Here's the change needed in app.py:

Edit c:\education\Codepath\ai110-module1show-gameglitchinvestigator-starter\app.py
Modified
What changed and why:

Wrapped st.text_input and the submit button in a st.form("guess_form"), replacing st.button with st.form_submit_button.
st.form batches all widget interactions and only triggers a rerun when the form is submitted — either by clicking the button or pressing Enter in the text field.
new_game and show_hint stay outside the form since they don't need to be part of the guess submission.``
I verified the fix was incorrect by running the app and confirming that pressing the "Enter" key still did not submit the guess, and the app continued to require clicking the "Submit Guess" button to submit the guess.``


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
--- I ran the app and ran several test cases to confirm that the behavior was correct.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
--- I ran the game and tested the hints for different guesses to confirm that the labels were correct. For example, if I guessed a number higher than the secret number, I expected to see the hint "Too High" and the label "📉 Go LOWER!" If I guessed a number lower than the secret number, I expected to see the hint "Too Low" and the label "📈 Go HIGHER!" Running these tests showed me that the logic in the check_guess function was now correct after applying the AI's suggestion.

- Did AI help you design or understand any tests? How?
--- I learned about something called playwright where Claude Code is able to test the app by simulating user interactions. Though this was not mentioned in the discussions, I found it super cool to work with. It helped me fix the the issue with the "Enter" key. 

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
--- It probably kept changing because the secret number was being generated on on every guess.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
--- Every time you type a guess and submit it, Streamlit reruns the whole script from top to bottom. This is resolved by using session state, which allows you to store values that persist across reruns. For example, you can store the secret number in session state so that it doesn't change every time the app reruns.

- What change did you make that finally gave the game a stable secret number?
--- I moved the code that generates the secret number into a block that only runs when the "New Game" button is clicked. This way, the secret number is only generated once per game and does not change on every guess.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
--- I think using Claude Code to debug and understand the bugs was really cool. I also enjoyed looking at the tests that Claude Code generated and I would continue to use that strategy in the future to help me design tests for my code.

- What is one thing you would do differently next time you work with AI on a coding task?
--- I would try to be more specific in my prompts to the AI to get more accurate suggestions. For example, when asking for help with the "Enter" key issue, I could have provided more context about how the app was currently handling input and what I expected to happen when pressing the "Enter" key.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
--- This project showed me that AI-generated code can be really helpful for fixing bugs and improving my code, but it's important to verify the suggestions and understand the underlying logic to ensure that the fixes are actually correct.