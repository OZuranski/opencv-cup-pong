# Cup-Pong Project

This project was inspired by the many times in my life playing cup pong with my family (with water) and we get into arguments about whether someone’s elbow crossed the edge of the table (**a federal crime in cup pong**).

## What it does
This small project uses OpenCV camera detection to detect **two markers** (at a time): one on the **edge of the table** and one on your **elbow**. The program finds the **center** of these trackers and monitors their **x** positions. If they cross:
- a **loud beep** plays, and  
- a **screenshot** is saved of you **CAUGHT RED-HANDED** breaking the rules.

## Exposure control
You can manually set exposure in the code beforehand **or** adjust it live while looking at the active camera window:
- Press **`z`** to lower exposure  
- Press **`x`** to raise exposure

_Current code includes general settings for my setup; you’ll likely need to tweak them._

## Cameras
The program has a list of camera **indexes** you can edit to match the cameras you have. Press **`t`** to toggle between cameras—ideally one at each end of the table.

You can also use the setup with **just one camera** if you prefer—just set the list of IDs accordingly.

## Markers & assets
Attached to the program are:
- PNGs for the trackers to print  
- `get_markers.py`, which I used to generate them

**I HEAVILY RECOMMEND USING A WHITE BORDER AROUND THE TRACKERS FOR BETTER TRACKING.**

## Install & run
There’s a `requirements.txt` file so you can set up the project with:

```bash
pip install -r requirements.txt
