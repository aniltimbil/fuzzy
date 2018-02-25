#Anil Timbil, Austin DiMartino, Andrew Godwin 
#February 25, 2018 
#Program 2 
#This program contains the code necessary for our xpilot ai bot to maneuver around
#different obstacles while also defending itself against other players in order to
#survive. The bot also has shooting and aiming capabilities to destroy other enemies
#as well. In this particular program we are using a fuzzy system in order to control
#the thrusting of the XPilot agent. Our linguistic variables are wall distance and speed.
#We have 3 fuzzy sets for both wall distance and speed. These fuzzy sets can be identified below.
    
#Importing the library 
import libpyAI as ai

#Define the equations for WallDistance
#the function that returns a degree of membership for the close fuzzy set
def close(distance):
  if distance <= 70:
    degMem = 1
  elif 70 < distance < 100:
    degMem= (-1/30)*distance +5/1.5
  elif distance >= 100:
    degMem = 0
  return degMem

#the function that returns a degree of membership for the medium fuzzy set
def medium(distance):
  if distance <= 75:
    degMem = 0
  elif 75 < distance < 105:
    degMem = (1/30)*distance -5/2
  elif 105 <= distance <= 120:
    degMem = 1
  elif 120 < distance < 150:
    degMem = (-1/30)*distance + 5
  elif distance >= 150:
    degMem = 0
  return degMem

#the function that returns a degree of membership for the far fuzzy set
def far(distance):
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
  return degMem


#the function that returns a degree of membership for the fast fuzzy set
def fast(speed):
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
  rightBottomWall = ai.wallFeeler(500,heading-140)
  leftBottomWall = ai.wallFeeler(500,heading+140)
  trackWall = ai.wallFeeler(500,tracking)
  trackWallLeft = ai.wallFeeler(500,tracking+30)
  trackWallRight = ai.wallFeeler(500,tracking-30)

  #Set variable right and left to determine which direction the ship should turn when
  #dealing with aiming 
  R=(heading-90)%360
  L=(heading+90)%360

  #Set variable to determine the direction  of the velocity of a shot from the enemy 
  shotDir = int(ai.shotVelDir(0))

  #Set a boolean variable to decide if we are in danger (we are in danger if a shot is
  #within the buffer and shotalert is below 50)
  Danger = shotDir!=-1 and ai.shotAlert(0)!=-1 and ai.shotAlert(0)<50
  shotFromLeft = -180 <= ai.angleDiff(heading, shotDir) <= -120 or 0 <= ai.angleDiff(heading, shotDir) <= 60 and ai.selfSpeed()<=6
  shotFromRight = 120 <= ai.angleDiff(heading, shotDir) <= 180 or -60 <= ai.angleDiff(heading, shotDir) <= 0 and ai.selfSpeed()<=6

  #fuzzy thrust rules to calculate risk value
  # Calculating the risk value for the backwall
  rule1 = min(max(close(trackWall),close(trackWallLeft),close(trackWallRight)),max(close(backWall),medium(backWall)))
  rule5 = min(fast(ai.selfSpeed()),close(backWall))
  rule6 = min(fast(ai.selfSpeed()),medium(backWall))
  rule7 = min(fast(ai.selfSpeed()),far(backWall))
  rule8 = min(medium(ai.selfSpeed()),close(backWall))
  rule9 = min(medium(ai.selfSpeed()),medium(backWall))
  rule10 = min(medium(ai.selfSpeed()),far(backWall))
  rule11 = min(slow(ai.selfSpeed()),close(backWall))
  rule12 = min(slow(ai.selfSpeed()),medium(backWall))
  rule13 = min(slow(ai.selfSpeed()),far(backWall))
  #Calculating the risk value for the side walls
  closestSideWall = min(leftWall,rightWall,leftBottomWall, rightBottomWall)
  rule2 = min(max(close(trackWall),close(trackWallLeft),close(trackWallRight)),max(close(closestSideWall), medium(closestSideWall)))
  rule14 = min(fast(ai.selfSpeed()),close(closestSideWall))
  rule15 = min(fast(ai.selfSpeed()),medium(closestSideWall))
  rule16 = min(fast(ai.selfSpeed()),far(closestSideWall))
  rule17 = min(medium(ai.selfSpeed()),close(closestSideWall))
  rule18 = min(medium(ai.selfSpeed()),medium(closestSideWall))
  rule19 = min(medium(ai.selfSpeed()),far(closestSideWall))
  rule20 = min(slow(ai.selfSpeed()),close(closestSideWall))
  rule21 = min(slow(ai.selfSpeed()),medium(closestSideWall))
  rule22 = min(slow(ai.selfSpeed()),far(closestSideWall))

  #weight calculation backwall
  numerator = (rule1 * 90 + rule5 * 45 + rule6 * 45 + rule7 *30 + rule8 *85 + rule9*35 + rule10 * 20 + rule11 *60 + rule12 *25 + rule13*10)
  denominator = (rule1 +rule5 + rule6 + rule7 + rule8 + rule9 + rule10 + rule11 + rule12 + rule13)
  backWallRisk = 0
  #weight calculation sidewalls
  numerator2 = (rule2 * 90 + rule14 * 45 + rule15 * 45 + rule16 *30 + rule17 *85 + rule18*35 + rule19 * 20 + rule20 *60 + rule21 *25 + rule22*10)
  denominator2 = (rule2 + rule14 + rule15 + rule16 + rule17 + rule18 + rule19 + rule20 + rule21 + rule22)
  sideWallRisk = 0

  if denominator >0:
    backWallRisk = numerator/denominator
    sideWallRisk = numerator2/denominator2

  #Thrust rules 
  if Danger:
    ai.thrust(1)    
  elif sideWallRisk >= 47 and frontWall >150 and frontWallleft >80 and frontWallright >80:
    ai.thrust(1)
  elif backWallRisk >= 47 and frontWall >150 and frontWallleft >80 and frontWallright >80:
    ai.thrust(1)
  elif ai.selfSpeed()<3 and frontWall >150:
    ai.thrust(1)

  #Set up more deciding variables for turning
  ai.setTurnSpeed(55.0)
  #If there is a wall between the enemy and our ship or if there is not a ship within the buffer.
  selfX= ai.selfX()
  selfY= ai.selfY()
  enemyX = ai.screenEnemyX(0)
  enemyY = ai.screenEnemyY(0)
  wallBetween = ai.wallBetween(selfX, selfY, enemyX, enemyY)
  #finds the closest wall to the ship
  closestLeftWall = min(leftWall, leftBottomWall)
  closestRightWall = min(rightWall, rightBottomWall)

  #Turn rules
  #If we have to turn more than 0 degrees to face the closest enemy and it will be quicker to
  #turn left towards the enemy than to turn right, then turn left and fire a shot.
  #If there is shot and we need to turn (we also thrust here because it's more efficient)
  if Danger and shotFromLeft:
    ai.turnRight(1)
    ai.thrust(1)    
  elif Danger and shotFromRight:
    ai.turnLeft(1)      
    ai.thrust(1)    
  #these 2 rules only fire if there is no wall between the ship and the enemy
  elif ai.aimdir(0)>=0 and angleDiff(L, ai.aimdir(0)) > angleDiff(R, ai.aimdir(0)) and wallBetween ==-1:
    ai.turnRight(1) 
  elif ai.aimdir(0)>=0 and angleDiff(L, ai.aimdir(0)) < angleDiff(R, ai.aimdir(0)) and wallBetween ==-1:
    ai.turnLeft(1)
  #To avoid walls
  elif frontWallleft <= frontWallright and frontWallleft<150 :
    ai.turnRight(1)
  elif frontWallright < frontWallleft and frontWallright<150:
    ai.turnLeft(1)   
  elif closestLeftWall <= closestRightWall and closestLeftWall<150 :
    ai.turnRight(1)
  elif closestRightWall < closestLeftWall and closestRightWall<150:
    ai.turnLeft(1)       
  elif leftWall <= rightWall and trackWall < 200:
    ai.turnRight(1)        
  elif leftWall > rightWall and trackWall < 200:
    ai.turnLeft(1)

  #fires a shot if the enemy is within 5 degrees of either direction of the heading of the ship
  if ai.aimdir(0)>=0 and  abs(ai.angleDiff(heading, ai.aimdir(0))) <= 5 and wallBetween ==-1:
    ai.fireShot()
 
#call the main function to initiate the loop
ai.start(AI_loop,["-name","FuzzyAAA","-join","localhost"])



















