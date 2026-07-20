import re

with open('tests/test_screenshot.py', 'r') as f:
    content = f.read()

# The exception is caught by the loop and printed, then continue is called.
# To break the loop we need to mock something that happens after the try-except block,
# or mock `time.sleep` such that it raises a specific error type that we don't catch (like KeyboardInterrupt)
# BUT the code uses `except Exception as e:`, so it catches almost everything except BaseException (like KeyboardInterrupt).
# Let's use KeyboardInterrupt.

content = content.replace('Exception("Break loop")', 'KeyboardInterrupt("Break loop")')
content = content.replace('with pytest.raises(Exception, match="Break loop"):', 'with pytest.raises(KeyboardInterrupt, match="Break loop"):')

with open('tests/test_screenshot.py', 'w') as f:
    f.write(content)
