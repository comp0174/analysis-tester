int main() {
  y = &x;
  x = 1;
  *y = 2;
  print(x);
}
