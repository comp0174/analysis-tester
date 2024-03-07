int main() {
  open(x);
  if (x > 1) {
    y = &x;
  } else {
    y = 0;
  }
  close(*y);
}
