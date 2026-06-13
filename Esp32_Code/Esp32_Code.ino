#define LED1 2
#define LED2 4
#define LED3 5
#define LED4 18
#define LED5 19

String cmd = "";

void setup()
{
  Serial.begin(115200);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
}

void runningAnimation()
{
  int leds[] = {LED1, LED2, LED3, LED4, LED5};

  for (int i = 0; i < 5; i++)
  {
    if (Serial.available())
      return;

    digitalWrite(leds[i], HIGH);
    delay(50);

    digitalWrite(leds[i], LOW);
  }
}

void blinkAnimation()
{
  for (int i = 0; i < 3; i++)
  {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    digitalWrite(LED3, HIGH);
    digitalWrite(LED4, HIGH);
    digitalWrite(LED5, HIGH);

    delay(200);

    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    digitalWrite(LED3, LOW);
    digitalWrite(LED4, LOW);
    digitalWrite(LED5, LOW);

    delay(200);
  }
}

void loop()
{
  if (Serial.available())
  {
    cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ANIMATION1")
    {
      runningAnimation();
    }
    else if (cmd == "ANIMATION2")
    {
      blinkAnimation();
    }
    else
    {
      if (cmd.length() == 5)
      {
        digitalWrite(LED1, cmd[0] == '1');
        digitalWrite(LED2, cmd[1] == '1');
        digitalWrite(LED3, cmd[2] == '1');
        digitalWrite(LED4, cmd[3] == '1');
        digitalWrite(LED5, cmd[4] == '1');
      }
    }
  }
}