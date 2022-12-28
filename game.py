from tkinter import *
from collections import deque
import random
import time

class HealthBar:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 100
        self.rectangle = self.canvas.create_rectangle(x, y, x+width, y+height, fill='green')
        self.canvas.tag_raise(self.rectangle)

    def update_health(self, new_health):
        self.health = new_health
        # Update the display of the health bar
        self.canvas.coords(self.rectangle, self.x, self.y, self.x + self.width * (self.health/100), self.y + self.height)


class Snake:
    def __init__(self, canvas,score_label):

        self.canvas = canvas

        self.body = [[0, 0]]
        self.dir = [1, 0]
        self.food = None
        self.over = False
        self.create_food()
        self.create_snake()
        self.bind_keys()
        self.points =0
        self.score_label = score_label
        self.delay = .5
        self.deadly_blocks = []
        self.delay = .5
        self.health = 100
        self.health_bar = HealthBar(canvas, 10, 10, 200, 20)
        self.deadly_counter = 0


    def update_health(self, new_health):
        self.health = new_health
        self.health_bar.update_health(self.health)

    def change_health(self, new_health):
        self.update_health(new_health)





    def create_deadly_block(self):

        x = random.randint(0, 19)
        y = random.randint(0, 19)
         # check if the deadly block is being spawned on the edge of the canvas
        if x == 0 or x == 19 or y == 0 or y == 19:
            # if so, pick new random coordinates
            self.create_deadly_block()

        else:

        
            deadly_block = self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill='purple')
            self.deadly_blocks.append(deadly_block)





    def game_loop(self):
        if self.over:
            return

        self.move()
        self.check_food_collision()
        
        self.check_boundaries()

        if self.health <= 0:
            self.game_over()
        else:
            self.canvas.after(int(1000*self.delay), self.game_loop)

        


    def update_score(self):
        self.points += 1
        self.score_label.config(text=f'Score: {self.points}')

    def create_food(self):
        x = random.randint(0, 19)
        y = random.randint(0, 19)
        self.food = self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill='red')

    def create_snake(self):
        self.rectangles = []
        x, y = self.body[0]
        rectangle = self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill='green')
        self.rectangles.append(rectangle)

    def bind_keys(self):
        self.canvas.bind_all('<KeyPress-w>', self.change_dir)
        self.canvas.bind_all('<KeyPress-s>', self.change_dir)
        self.canvas.bind_all('<KeyPress-a>', self.change_dir)
        self.canvas.bind_all('<KeyPress-d>', self.change_dir)

    def change_dir(self, event):
        if event.keysym == 'w':
            self.dir = [0, -1]
        elif event.keysym == 's':
            self.dir = [0, 1]
        elif event.keysym == 'a':
            self.dir = [-1, 0]
        elif event.keysym == 'd':
            self.dir = [1, 0]

    def move(self):
        # Get the current position of the snake's head

        self.deadly_counter += 1
        if self.deadly_counter % 25 == 0: #change modulo value to change the value of purple blocks
            self.create_deadly_block()
            self.deadly_counter = 0
        x, y = self.body[-1]

        for deadly_block in self.deadly_blocks:
            if self.canvas.coords(deadly_block) == self.canvas.coords(self.rectangles[0]):
                # reduce the snake's health by 10 and remove the deadly block from the canvas and list
                if self.health <= 0:
                    self.over = True
                self.update_health(self.health - 10)
                self.canvas.delete(deadly_block)
                self.deadly_blocks.remove(deadly_block)



      
        # Update the position of the snake's head based on the direction
        x += self.dir[0]
        y += self.dir[1]

        
        # Check if the snake has collided with a wall or its own body
        if x < 0 or x > 19 or y < 0 or y > 19 or [x, y] in self.body:
            if self.health <=0:

                self.over = True
            self.health -= 30
            self.change_health(self.health)
        # See if snake collided with food or not
  
            
        if self.food and [x, y] == self.get_coords(self.food):
            # Update the body list to reflect the new position of the snake
            self.body.append([x, y])
            # Create a new rectangle for the snake's body
            rectangle = self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill='green')
            self.rectangles.append(rectangle)
            # Delete the old food item
            self.canvas.delete(self.food)
            self.food = None

             # Randomly place a deadly block on the canvas
            x = random.randint(0, 19)
            y = random.randint(0, 19)
            self.deadly_block = self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill='black')
            # Create a new food item
            if self.health < 100:
                self.health +=10
                self.change_health( self.health)
            self.create_food()
            self.update_score()
            

        if [x, y] in self.deadly_blocks:
            self.over = True
        else:
            # Remove the old tail from the body list
            self.body = self.body[1:]
            # Update the body list to reflect the new position of the snake
            self.body.append([x, y])
            # Create a new rectangle for the snake's body
            rectangle = self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill='green')
            self.rectangles.append(rectangle)

            # Delete the old tail of the snake

            self.canvas.delete(self.rectangles[0])
            # Remove the old tail from the rectangles list
            self.rectangles = self.rectangles[1:]
            self.delay *=0

                
    def get_coords(self, item):
        coords = self.canvas.coords(item)
        # Convert the pixel coordinates to grid cell coordinates
        x = int(coords[0] // 20)
        y = int(coords[1] // 20)
        return [x, y]
            
    

    
def restart_game(root, canvas,score_label):
        # Delete the existing canvas
        canvas.delete("all")
        # Create a new Snake object and start a new game

        score_label.config(text='Score: 0')
        snake = Snake(canvas,score_label)
        starting_time = 100
        current_time = starting_time

        while not snake.over:
            if current_time> 50:
            

                current_time = starting_time- snake.points*2 #iNcrease time everytime the snake eats

            snake.move()
            root.update()
            root.after(current_time)
        # Display the "Game Over" text
        canvas.create_text(200, 200, text='Game Over', fill='red', font="Arial")




def main():
    root = Tk()
    root.title("Portal Snake - Kevin Wan")

    
    canvas = Canvas(root, width=400, height=400, bg='white')
    canvas.pack()
    score_label = Label(root, text='Score: 0')
    score_label.pack()
    snake = Snake(canvas,score_label)
   
    starting_time = 100
    current_time = starting_time



    
    while not snake.over:
        

        if current_time> 50:
            

            current_time = starting_time- snake.points*2 #iNcrease time everytime the snake eats



       
        
        


        # Update the snake's position
        snake.move()

        # Display the updated position of the snake

        
        root.update()

        # Delay the next move by 100 milliseconds
        root.after(current_time)
        

    # Display the "Game Over" text
    canvas.create_text(200, 200, text='Game Over', fill='red', font="Arial")
    restart_button = Button(root, text="Restart", command=lambda: restart_game(root, canvas,score_label))
    restart_button.pack()

    # Start the main event loop of the Tkinter application
    root.mainloop()


main()