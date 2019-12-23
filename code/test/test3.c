int func(a,b) {
    char* howtopointer = "abcdefghijk";
    int c = a - b;
    int d = a + b;
    int e = (int)(a / b);
    if(a == b) {
        return a;
    }
    else if(a >= b){
        return b;
    }
    return 0;
}
int main() {
    func(10, 20);
    return 1;
}