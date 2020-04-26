void func()
{
  try
  {
    throw 1;
  }
  catch(int a){

  }
  catch(int a){
  somecode();
  }
  cout << "No exception detected!" << endl;
  return;
}