//Pin definition
const int _OutPinLedBlue = 9;
const int _OutPinLedGreen = 10;
const int _OutPinLedRed = 11;

void setup()
{
  Serial.begin(9600);
  //defined IO
  pinMode(_OutPinLedBlue, OUTPUT);
  pinMode(_OutPinLedGreen, OUTPUT);
  pinMode(_OutPinLedRed, OUTPUT);
  
  digitalWrite(_OutPinLedBlue, LOW);
  digitalWrite(_OutPinLedGreen, LOW);
  digitalWrite(_OutPinLedRed, LOW);
  
  delay(5000);
}

void loop()
{
  int randNumberGreen = random(0, 255);
  Serial.println(randNumberGreen);
  int randNumberRed = random(0, 255);
  Serial.println(randNumberRed);
  int randNumberBlue = random(0, 255);
  Serial.println(randNumberBlue);
  
  analogWrite(_OutPinLedBlue, randNumberBlue); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  analogWrite(_OutPinLedGreen, randNumberGreen); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  analogWrite(_OutPinLedRed, randNumberRed); // impulsion largeur voulue sur la broche 0 = 0% et 255 = 100% haut
  delay(2000);
}
