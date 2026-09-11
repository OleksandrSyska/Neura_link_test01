import colors as c
import pygame as g
import random as r
import math as m
g.init()

SCW = 1900
SCH = 1000
gap = 50
size = 10
speed_modifier = 5
count = 20
gen_count = 1
mutation_difrence = 1.9
sc = g.display.set_mode((SCW, SCH))
#sc = g.display.set_mode((SCW, SCH), g.FULLSCREEN)


class NN():
    def __init__(self,x,y,color,dominant_dna):
        if dominant_dna == {}:
            self.dna = {
                "W1" : [], # 9*4= 36
                "B1" : [], # 4
        
                "W2" : [], # 4*4= 16
                "B2" : [], # 4
        
                "W3" : [], # 4*2= 8
                "B3" : []  # 2
            }

            for _ in range(36):
                self.dna["W1"].append( round(r.uniform(-1.00,1.00) ,2) )
            for _ in range(16):
                self.dna["W2"].append( round(r.uniform(-1.00,1.00) ,2) )
            for _ in range(8):
                self.dna["W3"].append( round(r.uniform(-1.00,1.00) ,2) )


            for _ in range(4):
                self.dna["B1"].append( round(r.uniform(-1.00,1.00) ,2) )
                self.dna["B2"].append( round(r.uniform(-1.00,1.00) ,2) )
            for _ in range(2):
                self.dna["B3"].append( round(r.uniform(-1.00,1.00) ,2) )

        else:
            self.dna = dominant_dna


        self.fitness = 0
        self.x = x
        self.y = y
        self.color = color
        self.rect = g.draw.rect(sc,self.color,(self.x,self.y,size,size))


    def predict(self,inputs): # pred x,y,d ; victim x,y,d ; partner x,y,d
        h0 = 0
        h1 = 0
        h2 = 0
        h3 = 0
        h4 = 0
        h5 = 0
        h6 = 0
        h7 = 0
        h8 = 0
        h9 = 0
        #first row
        for i in range(9):
            h0 += inputs[i] * self.dna["W1"][i]
        for i in range(9):
            h1 += inputs[i] * self.dna["W1"][i+9]
        for i in range(9):
            h2 += inputs[i] * self.dna["W1"][i+18]
        for i in range(9):
            h3 += inputs[i] * self.dna["W1"][i+27]

    
        h0 += self.dna["B1"][0]
        h1 += self.dna["B1"][1]
        h2 += self.dna["B1"][2]
        h3 += self.dna["B1"][3]
        h0 = m.tanh(h0)
        h1 = m.tanh(h1)
        h2 = m.tanh(h2)
        h3 = m.tanh(h3)
        row1_Hs = [h0,h1,h2,h3]

        #second row
        for i in range(4):
            h4 += row1_Hs[i] * self.dna["W2"][i]
        for i in range(4):
            h5 += row1_Hs[i] * self.dna["W2"][i+4]
        for i in range(4):
            h6 += row1_Hs[i] * self.dna["W2"][i+8]
        for i in range(4):
            h7 += row1_Hs[i] * self.dna["W2"][i+12]

        
        h4 += self.dna["B2"][0]
        h5 += self.dna["B2"][1]
        h6 += self.dna["B2"][2]
        h7 += self.dna["B2"][3]
        h4 = m.tanh(h4)
        h5 = m.tanh(h5)
        h6 = m.tanh(h6)
        h7 = m.tanh(h7)
        row2_Hs = [h4,h5,h6,h7]

        #third row
        for i in range(4):
            h8 += row2_Hs[i] * self.dna["W3"][i]
        for i in range(4):
            h9 += row2_Hs[i] * self.dna["W3"][i+4]

        h8 += self.dna["B3"][0]
        h9 += self.dna["B3"][1]
        h8 = m.tanh(h8)
        h9 = m.tanh(h9)

        new_x = self.x + h8 * speed_modifier
        if 0 <= new_x <= SCW - size:
            self.x = new_x

        new_y = self.y + h9 * speed_modifier
        if 0 <= new_y <= SCH - size:
            self.y = new_y

    def mutate(self):
        how_many_mutations = r.randint(0, 30)
        already_mutated = []

        for _ in range(how_many_mutations):
            chosen = r.randint(0, 69)
            while chosen in already_mutated:
                chosen = r.randint(0, 69)

            already_mutated.append(chosen)

            if 0 <= chosen <= 35:
                self.dna["W1"][chosen] += round(r.uniform(-mutation_difrence, mutation_difrence), 2)

            elif 36 <= chosen <= 39:
                self.dna["B1"][chosen - 36] += round(r.uniform(-mutation_difrence, mutation_difrence), 2)

            elif 40 <= chosen <= 55:
                self.dna["W2"][chosen - 40] += round(r.uniform(-mutation_difrence, mutation_difrence), 2)

            elif 56 <= chosen <= 59:
                self.dna["B2"][chosen - 56] += round(r.uniform(-mutation_difrence, mutation_difrence), 2)

            elif 60 <= chosen <= 67:
                self.dna["W3"][chosen - 60] += round(r.uniform(-mutation_difrence, mutation_difrence), 2)

            elif 68 <= chosen <= 69:
                self.dna["B3"][chosen - 68] += round(r.uniform(-mutation_difrence, mutation_difrence), 2)

                
    def draw(self):
        self.rect.topleft = (self.x, self.y)
        g.draw.rect(sc, self.color, self.rect)

    def eat(self, victims):
        for victim in victims[:]:
            if self.rect.colliderect(victim.rect):
                victims.remove(victim)
                self.fitness += 1
reds = []
blues = []
greens = []
yellows = []

'''

for _ in range(count):
    red = NN(
        r.randint(gap,SCW//2-gap),
        r.randint(gap,SCH//2-gap),
        c.RED,
        {}
        )
    reds.append(red)
for _ in range(count):
    blue = NN(
        r.randint(gap,SCW//2-gap),
        r.randint(SCH//2+gap,SCH-gap),
        c.BLUE,
        {}
        )
    blues.append(blue)
for _ in range(count):
    green = NN(
        r.randint(SCW//2+gap,SCW-gap),
        r.randint(gap,SCH//2-gap),
        c.GREEN,
        {}
        )
    greens.append(green)
for _ in range(count):
    yellow = NN(
        r.randint(SCW//2+gap,SCW-gap),
        r.randint(SCH//2+gap,SCH-gap),
        c.GOLD,
        {}
        )
    yellows.append(yellow)
'''
for _ in range(count):
    red = NN(
        r.randint(gap,SCW-gap),
        r.randint(gap,SCH-gap),
        c.RED,
        {}
        )
    reds.append(red)
for _ in range(count):
    blue = NN(
        r.randint(gap,SCW-gap),
        r.randint(gap,SCH-gap),
        c.BLUE,
        {}
        )
    blues.append(blue)
for _ in range(count):
    green = NN(
        r.randint(gap,SCW-gap),
        r.randint(gap,SCH-gap),
        c.GREEN,
        {}
        )
    greens.append(green)
for _ in range(count):
    yellow = NN(
        r.randint(gap,SCW-gap),
        r.randint(gap,SCH-gap),
        c.GOLD,
        {}
        )
    yellows.append(yellow)

def distance_calc(a,b):
    dif_x = a.x - b.x
    dif_y = a.y - b.y
    return m.sqrt(dif_x**2 + dif_y**2)
    
def target_info(me, target):
    dx = target.x - me.x
    dy = target.y - me.y

    distance = m.sqrt(dx**2 + dy**2)

    if distance == 0:
        return 0, 0, 0

    direction_x = dx / distance
    direction_y = dy / distance

    max_distance = m.sqrt(SCW**2 + SCH**2)
    distance = distance / max_distance

    return distance, direction_x, direction_y
def find_nearest(me, creatures):
    nearest = None
    nearest_distance = float("inf")

    for creature in creatures:
        distance = distance_calc(me, creature)

        if distance < nearest_distance:
            nearest_distance = distance
            nearest = creature

    return nearest
def find_dominant(targets):
    best_fitness = 0
    best_index = 0
    for i in targets:
        if i.fitness > best_fitness:
            best_fitness = i.fitness
            best_index = targets.index(i)

    return targets[best_index].dna


clock = g.time.Clock()


FPS = 60


print("curent gen: " + str(gen_count))
while 1:
    for event in g.event.get():
        if event.type == g.KEYDOWN:
            if event.key == g.K_ESCAPE:
                exit()
            if event.key == g.K_SPACE:
                # NEW GEN
                gen_count += 1
                print("curent gen: " + str(gen_count))
                all_creatures = reds + greens + yellows + blues
                dominatn_dna = find_dominant(all_creatures)
                '''
                dominant_dna_red = find_dominant(reds)
                dominant_dna_green = find_dominant(greens)
                dominant_dna_blue = find_dominant(blues)
                dominant_dna_yellow = find_dominant(yellows)
                '''
                reds.clear()
                greens.clear()
                yellows.clear()
                blues.clear()
                '''
                for _ in range(count):
                    red = NN(
                        r.randint(gap,SCW//2-gap),
                        r.randint(gap,SCH//2-gap),
                        c.RED,
                        dominatn_dna
                        )
                    reds.append(red)
                for _ in range(count):
                    blue = NN(
                        r.randint(gap,SCW//2-gap),
                        r.randint(SCH//2+gap,SCH-gap),
                        c.BLUE,
                        dominatn_dna
                        )
                    blues.append(blue)
                for _ in range(count):
                    green = NN(
                        r.randint(SCW//2+gap,SCW-gap),
                        r.randint(gap,SCH//2-gap),
                        c.GREEN,
                        dominatn_dna
                        )
                    greens.append(green)
                for _ in range(count):
                    yellow = NN(
                        r.randint(SCW//2+gap,SCW-gap),
                        r.randint(SCH//2+gap,SCH-gap),
                        c.GOLD,
                        dominatn_dna
                        )
                    yellows.append(yellow)
                '''
                for _ in range(count):
                    red = NN(
                        r.randint(gap,SCW-gap),
                        r.randint(gap,SCH-gap),
                        c.RED,
                        dominatn_dna
                        )
                    reds.append(red)
                for _ in range(count):
                    blue = NN(
                        r.randint(gap,SCW-gap),
                        r.randint(gap,SCH-gap),
                        c.BLUE,
                        dominatn_dna
                        )
                    blues.append(blue)
                for _ in range(count):
                    green = NN(
                        r.randint(gap,SCW-gap),
                        r.randint(gap,SCH-gap),
                        c.GREEN,
                        dominatn_dna
                        )
                    greens.append(green)
                for _ in range(count):
                    yellow = NN(
                        r.randint(gap,SCW-gap),
                        r.randint(gap,SCH-gap),
                        c.GOLD,
                        dominatn_dna
                        )
                    yellows.append(yellow)








    #### 
    sc.fill(c.BLACK)
    nearest = 99999.9
    distance_predator = 0
    distance_victim = 0
    distance_partner = 0

    for i in reds:
        predator = find_nearest(i, blues)
        victim = find_nearest(i, greens)
        partner = find_nearest(i, yellows)

        pred_d, pred_x, pred_y = 0, 0, 0
        vict_d, vict_x, vict_y = 0, 0, 0
        part_d, part_x, part_y = 0, 0, 0

        if predator:
            pred_d, pred_x, pred_y = target_info(i, predator)

        if victim:
            vict_d, vict_x, vict_y = target_info(i, victim)

        if partner:
            part_d, part_x, part_y = target_info(i, partner)

        i.predict([
            pred_d, pred_x, pred_y,
            vict_d, vict_x, vict_y,
            part_d, part_x, part_y
        ])

        i.predict([
            pred_d, pred_x, pred_y,
            vict_d, vict_x, vict_y,
            part_d, part_x, part_y
        ])
    for i in blues:
        predator = find_nearest(i, yellows)
        victim = find_nearest(i, reds)
        partner = find_nearest(i, greens)

        pred_d, pred_x, pred_y = 0, 0, 0
        vict_d, vict_x, vict_y = 0, 0, 0
        part_d, part_x, part_y = 0, 0, 0

        if predator:
            pred_d, pred_x, pred_y = target_info(i, predator)

        if victim:
            vict_d, vict_x, vict_y = target_info(i, victim)

        if partner:
            part_d, part_x, part_y = target_info(i, partner)

        i.predict([
            pred_d, pred_x, pred_y,
            vict_d, vict_x, vict_y,
            part_d, part_x, part_y
        ])
    for i in greens:
        predator = find_nearest(i, reds)
        victim = find_nearest(i, yellows)
        partner = find_nearest(i, blues)

        pred_d, pred_x, pred_y = 0, 0, 0
        vict_d, vict_x, vict_y = 0, 0, 0
        part_d, part_x, part_y = 0, 0, 0

        if predator:
            pred_d, pred_x, pred_y = target_info(i, predator)

        if victim:
            vict_d, vict_x, vict_y = target_info(i, victim)

        if partner:
            part_d, part_x, part_y = target_info(i, partner)

        i.predict([
            pred_d, pred_x, pred_y,
            vict_d, vict_x, vict_y,
            part_d, part_x, part_y
        ])  
    for i in yellows:
        predator = find_nearest(i, greens)
        victim = find_nearest(i, blues)
        partner = find_nearest(i, reds)

        pred_d, pred_x, pred_y = 0, 0, 0
        vict_d, vict_x, vict_y = 0, 0, 0
        part_d, part_x, part_y = 0, 0, 0

        if predator:
            pred_d, pred_x, pred_y = target_info(i, predator)

        if victim:
            vict_d, vict_x, vict_y = target_info(i, victim)

        if partner:
            part_d, part_x, part_y = target_info(i, partner)

        i.predict([
            pred_d, pred_x, pred_y,
            vict_d, vict_x, vict_y,
            part_d, part_x, part_y
        ])

    for i in reds:
        i.eat(greens)
        i.draw()

    for i in greens:
        i.eat(yellows)
        i.draw()

    for i in blues:
        i.eat(reds)
        i.draw()

    for i in yellows:
        i.eat(blues)
        i.draw()


    g.display.update()
    clock.tick(FPS)