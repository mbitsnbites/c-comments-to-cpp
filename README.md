## ⚠️ This repository has moved to: https://gitlab.com/mbitsnbites/c-comments-to-cpp

# C comments to C++

This tool converts C style comments to C++ style comments.

By default the program expects the source file on STDIN, and writes the result
to STDOUT (it is also possible to pass the paths of the input and ouput files
as command line options).

You can also alter the behavior of the conversion by passing command line
options.

For more information, run `c-comments-to-cpp.py --help`

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

Then `c-comments-to-cpp.py test.cpp` outputs:

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

