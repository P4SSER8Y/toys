#include <type_traits>

#ifndef MIN_VALUE
#define MIN_VALUE 2
#endif

#ifndef MAX_VALUE
#define MAX_VALUE 1024
#endif

constexpr bool f(const int i, const int n) {
  if (n < 2)
    return false;
  if (i * i > n)
    return true;
  if (n % i == 0)
    return false;
  if (i == 2)
    return f(3, n);
  return f(i + 2, n);
}

constexpr bool is_prime(int i) { return f(2, i); }

template <int N, bool F> struct number {};
template <int N> struct number<N, false> { typedef bool is_prime; };

template <int N> void f() { typename number<N, is_prime(N)>::is_prime foobar; }

template <int I, int N> typename std::enable_if<(I > N)>::type build() {}

template <int I, int N> typename std::enable_if<(I <= N)>::type build() {
  f<I>();
  build<I + 1, N>();
}

int main() {
  build<MIN_VALUE, MAX_VALUE>();
  return 0;
}
