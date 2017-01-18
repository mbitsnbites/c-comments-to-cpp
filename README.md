# C comments to C++

This tool converts C style comments to C++ style comments.

The program expects the source file on STDIN, and writes the result to STDOUT.

For example, if this is `test.cpp`:

```c++
  /*****************************************************************************
  * This is a big comment.
  *****************************************************************************/

  /**
  * @brief Return value for all library functions.
  */
  typedef enum {
    STATUS_FAIL = 0, /*!< Failure (zero). */
    STATUS_OK = 1    /*!< Success
                          (non-zero). */
  } status_t;

  void foo() {
    /* Print a message. */
    printf("Hello! \"/* This is not a comment! */\"\n"); /* ...but this is. */
  }
```

Then `cat test.cpp | c-comments-to-cpp.py` outputs:

```c++
  //****************************************************************************
  // This is a big comment.
  //****************************************************************************

  /// @brief Return value for all library functions.
  typedef enum {
    STATUS_FAIL = 0, ///< Failure (zero).
    STATUS_OK = 1    ///< Success
                     ///< (non-zero).
  } status_t;

  void foo() {
    // Print a message.
    printf("Hello! \"/* This is not a comment! */\"\n"); // ...but this is.
  }
```

