from spade import message
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
import time
from spade.message import Message
from random import randrange

class Player(Agent): 
    class GameBehaviour(FSMBehaviour):
        async def on_start(self):
            print(f"{self.agent.name}: Ulazim u igru!")

        async def on_end(self):
            print(f"{self.agent.name}: Izlazim iz igre!")

    class TakeCard(State):
        async def run(self):           
            msg = await self.receive(timeout=120)
            if msg.body == "lost":
                print(f"{self.agent.name}: Arrrrghhh!!!")
                await self.agent.stop()
            else:
                numberOfOpponentCards = int(msg.body)
                msg = Message(to=self.agent.sendTo, body=str(randrange(numberOfOpponentCards)))
                print(f"{self.agent.name}: Uzimam {int(msg.body) + 1}. kartu")
                time.sleep(2)
                await self.send(msg)

                msg = await self.receive(timeout=120)
                self.agent.addCardToHand(msg.body)
                self.set_next_state("Remove")

    class SendCard(State):
        async def run(self):
            cardsNum = len(self.agent.hand)
            if cardsNum == 0:
                print(f"{self.agent.name}: Pobijedio sam! {self.agent.sendTo} je Crni Petar!")
                await self.send(Message(to=self.agent.sendTo, body="lost"))
                await self.agent.stop()
            else:
                msg = Message(to=self.agent.sendTo, body=str(cardsNum))
                print(f"{self.agent.name} Imam {len(self.agent.hand)} karti.")
                time.sleep(2)
                await self.send(msg)

                msg = await self.receive(timeout=120)
                cardIndex = int(msg.body)
                card = self.agent.hand[cardIndex]
                
                msg = Message(to=self.agent.sendTo, body=card)
                self.agent.hand.remove(card)
                time.sleep(2)
                print(f"{self.agent.name}: Uzeo si kartu {card}.")
                await self.send(msg)

                self.set_next_state("Remove")

    class RemovePairs(State):
        async def run(self):
            print(f"{self.agent.name}: Odbacujem sve parove iz ruke!")
            self.agent.hand = list(filter(lambda x: self.agent.hand.count(x) == 1, self.agent.hand))
            time.sleep(2)
            self.agent.printHand()           
            if self.agent.previousState == "Send":
                self.agent.previousState = "Take"
                self.set_next_state("Take")
            else:
                self.agent.previousState = "Send"
                self.set_next_state("Send")
                

    async def setup(self):
        fsm = self.GameBehaviour()
        fsm.add_state(name="Take", state=self.TakeCard())
        fsm.add_state(name="Remove", state=self.RemovePairs(), initial=True)
        fsm.add_state(name="Send", state=self.SendCard())

        fsm.add_transition(source="Remove", dest="Take")
        fsm.add_transition(source="Remove", dest="Send")
        fsm.add_transition(source="Take", dest="Remove")
        fsm.add_transition(source="Send", dest="Remove")

        self.add_behaviour(fsm)

    def __init__(self, jid, password, goesFirst, sendTo):
        super().__init__(jid, password)
        self.hand = []
        self.previousState = "Send" if goesFirst else "Take"
        self.sendTo = sendTo

    def printHand(self):
        print(f"{self.name}: U ruci imam: {self.hand}")

    def addCardToHand(self, card):
        self.hand.append(card)