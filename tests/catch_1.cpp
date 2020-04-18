void main(){
MyData md;
try {
   // Code that could throw an exception
   md = GetNetworkResource();
}
catch (const networkIOException& e) {
   // Code that executes when an exception of type
   // networkIOException is thrown in the try block
   // ...
   // Log error message in the exception object
}
catch (const myDataFormatException& e) {
   // Code that handles another exception type
   // ...
}
}