# C comments to C++

This tool converts C style comments to C++ style comments.

The program expects the source file on STDIN, and writes the result to STDOUT.

For example, if this is `test.cpp`:

```c++
  static int some_var;  /* This is a static variable */

  /**
  * @brief Some function.
  * @param x The first argument.
  */
  void cool_fun(int x) {
    ...
  }
```

Then `cat test.cpp | c-comments-to-cpp.py` outputs:

```c++
  static int some_var;  // This is a static variable

  /// @brief Some function.
  /// @param x The first argument.
  void cool_fun(int x) {
    ...
  }
```

