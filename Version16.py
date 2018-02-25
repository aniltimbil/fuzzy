#Anil Timbil, Austin DiMartino, Andrew Godwin 

#February 5, 2018 

#Program 1 

#This program contains the code necessary for our xpilot ai bot to maneuver around different obstacles while also defending itself against other players in order to survive. The bot also has shooting and aiming capabilities to destroy other enemies as well. 

    



#Importing the library 

import libpyAI as ai



#Define the equations for WallDistance
#the function that returns a degree of membership for the close fuzzy set
def close(distance):
  print("working close")

  if distance <= 45:

    degMem = 1

  elif 45 < distance < 75:

    degMem= (-1/30)*distance +5/2

  elif distance >= 75:

    degMem = 0

  return degMem


#the function that returns a degree of membership for the medium fuzzy set
def medium(distance):
  print("working medium")
  if distance <= 37.5:

    degMem = 0

  elif 37.5 < distance < 67.5:

    degMem = (1/30)*distance -5/4

  elif 67.5 <= distance <= 120:

    degMem = 1

  elif 120 < distance < 150:

    degMem = (-1/30)*distance + 5

  elif distance >= 150:

    degMem = 0

  return degMem


#the function that returns a degree of membership for the far fuzzy set
def far(distance):
  print("working far")

  if distance <138:

    degMem = 0

  elif 138 <= distance <= 168:

    degMem = (1/30)*distance -23/5

  elif distance > 168:

    degMem = 1

  return degMem



#Define the equations for speed 
#the function that returns a degree of membership for the slow fuzzy set
def slow(speed):


  if speed <= 2.5:

    degMem = 1

  elif 2.5 < speed < 5:

    degMem= (-1/2.5)*speed +2

  elif speed >= 5:

    degMem = 0
  print("working slow")
  return degMem


#the function that returns a degree of membership for the fast fuzzy set
def fast(speed):
  print("working fast")

  if speed <3:

    degMem = 0

  elif 3 <= speed <= 5.5:

    degMem = (1/2.5)*speed -1.2

  elif speed > 5.5:

    degMem = 1

  return degMem

#Defines the formula to find the true difference in angles. 

def angleDiff(a1,a2):

  return 180 - abs( abs(a1 - a2) - 180)



#Defines the loop that the program will pass through over several frames

def AI_loop():

  #Release keys

  ai.thrust(0)

  ai.turnLeft(0)

  ai.turnRight(0)

  #Set variables for walls 

  heading = int(ai.selfHeadingDeg())

  tracking = int(ai.selfTrackingDeg())

  frontWall = ai.wallFeeler(500,heading)

  #Adding more wall feelers/sensors 

  frontWallleft = ai.wallFeeler(500,heading+45)

  frontWallright = ai.wallFeeler(500,heading-45)

  leftWall = ai.wallFeeler(500,heading+90)

  rightWall = ai.wallFeeler(500,heading-90)

  backWall = ai.wallFeeler(500,heading-180)

  rightBottomWall = ai.wallFeeler(500,heading+220)

  leftBottomWall = ai.wallFeeler(500,heading+140)

  trackWall = ai.wallFeeler(500,tracking)

  #Tracking enemy location and direction

  enemyDistance = ai.enemyDistance(0)  #(returns 9999.0 if no enemy is within the buffer of our ship)
  print(enemyDistance)

  WallDistBwEnemy = 0

  #If ai.enemyDistance(0) returns a valid distance, and the ship needs to turn 0 or more degrees to face the closest enemy...

  if enemyDistance != 9999.0 and ai.aimdir(0)>=0:

    #then use the wallFeeler to figure out if there is a wall between you and the enemy 

    WallDistBwEnemy = ai.wallFeeler(int(enemyDistance), ai.aimdir(0))

  #Set variable right and left to determine which direction the ship should turn when dealing with aiming 

  R=(heading-90)%360

  L=(heading+90)%360



  #Set variable to determine the direction  of the velocity of a shot from the enemy 

  shotDir = int(ai.shotVelDir(0))

  #If the shot danger is less than 50 (where the lower value represents a greater shot danger) and the shot is not within range...

  if shotDir!=-1 and ai.shotAlert(0)!=-1 and ai.shotAlert(0)<50:

    #Turn and thrust if the shot is coming from the front or the back

    if -180 <= ai.angleDiff(heading, shotDir) <= -120 or 0 <= ai.angleDiff(heading, shotDir) <= 60 and ai.selfSpeed()<=6:

      ai.turnRight(1)

      ai.thrust(1)  

    elif 120 <= ai.angleDiff(heading, shotDir) <= 180 or -60 <= ai.angleDiff(heading, shotDir) <= 0 and ai.selfSpeed()<=6: 

      ai.turnLeft(1)

      ai.thrust(1) 

    #Just thrust if the shot is relatively perpendicular to the ship

    else:

      ai.thrust(1)



  else:

  #fuzzy thrust rules to calculate risk value

    rule1 = min(close(trackWall),max(close(backWall),medium(backWall)))


    
    rule5 = min(fast(ai.selfSpeed()),close(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule6 = min(fast(ai.selfSpeed()),medium(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))
    
 
    rule7 = min(fast(ai.selfSpeed()),far(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule8 = min(medium(ai.selfSpeed()),close(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule9 = min(medium(ai.selfSpeed()),medium(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule10 = min(medium(ai.selfSpeed()),far(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule11 = min(slow(ai.selfSpeed()),close(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule12 = min(slow(ai.selfSpeed()),medium(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))

    rule13 = min(slow(ai.selfSpeed()),far(min(leftWall,rightWall,leftBottomWall, rightBottomWall, backWall)))
#    print(rule1,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13)

    #weight calculation
    #numerator = (rule1 * 90 + rule5 * 95 + rule6 * 45 + rule7 *30 + rule8 *85 + rule9*35 + rule10 * 20 + rule11 *75 + rule12 *25 + rule13*10)
    numerator = (rule1 * 90 + rule5 * 95 + rule6 * 45 + rule7 *30 + rule8 *85 + rule9*35 + rule10 * 20 + rule11 *60 + rule12 *25 + rule13*10)

    denominator = (rule1 + rule5 + rule6 + rule7 + rule8 + rule9 + rule10 + rule11 + rule12 + rule13)

    weight = 0
    if denominator >0:
      weight = numerator/denominator
    print(weight)

    #Thrust based on the risk value
#    if ai.selfSpeed()==0 and backWall <= 30:
#      ai.setPower(15.0)
#      ai.thrust(1)

    if weight >= 75:
      ai.thrust(1)
    elif ai.selfSpeed()<3 and frontWall >100:
      ai.thrust(1)




  #Turn rules

    #sets the turn speed 

    ai.setTurnSpeed(45.0)

    #If there is a wall between the enemy and our ship or if there is not a ship within the buffer.
    selfX= ai.selfX()
    selfY= ai.selfY()
    enemyX = ai.screenEnemyX(0)
    enemyY = ai.screenEnemyY(0)
    wallBetween = ai.wallBetween(selfX, selfY, enemyX, enemyY)
    #print(wallBetween)
    #finds the closest wall to the ship
    closestLeftWall = min(leftWall, leftBottomWall)
    closestRightWall = min(rightWall, rightBottomWall)

    #If we have to turn more than 0 degrees to face the closest enemy and it will be quicker to turn left towards the enemy than to turn right, then turn left and fire a shot.
    #these first 2 rules only fire if there is no wall between the ship and the enemy
    if ai.aimdir(0)>=0 and angleDiff(L, ai.aimdir(0)) > angleDiff(R, ai.aimdir(0)) and wallBetween ==-1:

      ai.turnRight(1) 

    elif ai.aimdir(0)>=0 and angleDiff(L, ai.aimdir(0)) < angleDiff(R, ai.aimdir(0)) and wallBetween ==-1:

      ai.turnLeft(1)

    elif frontWallleft <= frontWallright and frontWallleft<300 :

      ai.turnRight(1)

    elif frontWallright <= frontWallleft and frontWallright<300:

      ai.turnLeft(1)   
   

    elif closestLeftWall <= closestRightWall and closestLeftWall<300 :

      ai.turnRight(1)

    elif closestRightWall <= closestLeftWall and closestRightWall<300:

      ai.turnLeft(1)       
    elif leftWall < rightWall and trackWall < 200:

      ai.turnRight(1)        

    elif leftWall > rightWall and trackWall < 200:

      ai.turnLeft(1)

    #fires a shot if the enemy is within 5 degrees of either direction of the heading of the ship
    if ai.aimdir(0)>=0 and  abs(ai.angleDiff(heading, ai.aimdir(0))) <= 5 and wallBetween ==-1:

      ai.fireShot()


    
      





  

#call the main function to initiate the loop

ai.start(AI_loop,["-name","DumboAAANew","-join","localhost"])



















