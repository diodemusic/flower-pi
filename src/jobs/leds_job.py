import RPi.GPIO as GPIO  # pyright: ignore[reportMissingModuleSource]
import asyncio

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(0, GPIO.OUT, initial=GPIO.LOW)


async def leds_job():
    while True:
        GPIO.output(8, GPIO.HIGH)
        await asyncio.sleep(1)
        GPIO.output(8, GPIO.LOW)
        await asyncio.sleep(1)
