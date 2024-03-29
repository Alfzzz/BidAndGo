#############Libraries#######################################################
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont
from datetime import datetime,timedelta
from solcx import compile_source
import time
from web3 import Web3
import threading
import os 
#######################GUI Class#########################################################
# Create a subclass of QMainWindow to setup the project
class CryptoProject(QMainWindow):
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle("Tec Community Peer to Peer Ridesharing") #Title
        self.setFixedSize(560,680)  #Windows size
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
##################Driver Credentials####################################################

        #Driver Creddential Title#
        self.driverCredentialsTitle = QVBoxLayout()
        self.driverCredentialsText=QLabel('Driver credentials:')
        self.driverCredentialsText.setFont(QFont('Arial',20))
        self.driverCredentialsTitle.addWidget(self.driverCredentialsText)
        self.generalLayout.addLayout(self.driverCredentialsTitle)

        #Driver Address and key#
        driverCredentialsLayout = QGridLayout()
        self.driverAddressText=QLabel('Address:')
        self.driverAddressText.setFont(QFont('Arial',15))
        self.driverKeyText=QLabel('Key:')
        self.driverKeyText.setFont(QFont('Arial',15))
        self.driverAddressEdit=QLineEdit("")
        self.driverKeyEdit=QLineEdit("")
        driverCredentialsLayout.addWidget(self.driverAddressText, 0, 0)
        driverCredentialsLayout.addWidget(self.driverAddressEdit, 0, 1)
        driverCredentialsLayout.addWidget(self.driverKeyText, 0, 2)
        driverCredentialsLayout.addWidget(self.driverKeyEdit, 0, 3)
        self.generalLayout.addLayout(driverCredentialsLayout)

        #Driver Login button#
        self.driverLogin = QVBoxLayout()
        self.driverLoginBttn=QPushButton("Driver login!")
        self.driverLoginBttn.setFont(QFont('Arial',10))
        self.driverLoginBttn.clicked.connect(self.driverLoginFunc)
        self.driverLogin.addWidget(self.driverLoginBttn)
        self.generalLayout.addLayout(self.driverLogin)
##################Passenger Credentials####################################################

        #Pssanger Credential Title#
        self.passangerCredentialsTitle = QVBoxLayout()
        self.passangerCredentialsText=QLabel('Passenger credentials:')
        self.passangerCredentialsText.setFont(QFont('Arial',20))
        self.passangerCredentialsTitle.addWidget(self.passangerCredentialsText)
        self.generalLayout.addLayout(self.passangerCredentialsTitle)

        #Passenger Address and key#
        passengerCredentialsLayout = QGridLayout()
        self.passengerAddressText=QLabel('Address:')
        self.passengerAddressText.setFont(QFont('Arial',15))
        self.passengerKeyText=QLabel('Key:')
        self.passengerKeyText.setFont(QFont('Arial',15))
        self.passengerAddressEdit=QLineEdit("")
        self.passengerKeyEdit=QLineEdit("")
        passengerCredentialsLayout.addWidget(self.passengerAddressText, 0, 0)
        passengerCredentialsLayout.addWidget(self.passengerAddressEdit, 0, 1)
        passengerCredentialsLayout.addWidget(self.passengerKeyText, 0, 2)
        passengerCredentialsLayout.addWidget(self.passengerKeyEdit, 0, 3)
        self.generalLayout.addLayout(passengerCredentialsLayout)

        #Passenger Login button#
        self.passengerLogin = QVBoxLayout()
        self.passengerLoginBttn=QPushButton("Passenger login!")
        self.passengerLoginBttn.setFont(QFont('Arial',10))
        self.passengerLoginBttn.clicked.connect(self.passengerLoginFunc)
        self.passengerLogin.addWidget(self.passengerLoginBttn)
        self.generalLayout.addLayout(self.passengerLogin)

##################Driver ride settings##########################################  

        #Send Ride offer Title#
        self.driverTitle = QVBoxLayout()
        self.sendRideOfferText=QLabel('Send ride offer:')
        self.sendRideOfferText.setFont(QFont('Arial',20))
        self.driverTitle.addWidget(self.sendRideOfferText)
        self.generalLayout.addLayout(self.driverTitle)

        #Ride settings#
        driverLayout = QGridLayout()
        self.locations=QComboBox()
        self.locations.addItems(["Coyoacan","Tlalpan","BenitoJuarez","Tlahuac","Iztapalapa"])
        self.seats=QComboBox()
        self.seats.addItems(["1","2","3","4"])
        self.dateTime = QDateTimeEdit(QDateTime(datetime.now().year,datetime.now().month,datetime.now().day,datetime.now().hour,datetime.now().minute))
        self.priceText=QLabel('Price:')
        self.priceText.setFont(QFont('Arial',15))
        self.locationText=QLabel('Location:')
        self.locationText.setFont(QFont('Arial',15))
        self.seatsText=QLabel('Seats:')
        self.seatsText.setFont(QFont('Arial',15))
        self.dateAndTimeText=QLabel('Date and Time:')
        self.dateAndTimeText.setFont(QFont('Arial',15))
        self.durationText=QLabel('Duration(Minutes):')
        self.durationText.setFont(QFont('Arial',15))
        self.priceEdit=QLineEdit("")
        self.durationEdit=QLineEdit("")
        driverLayout.addWidget(self.priceText, 0, 0)
        driverLayout.addWidget(self.priceEdit, 0, 1)
        driverLayout.addWidget(self.locationText, 0, 2)
        driverLayout.addWidget(self.locations, 0, 3)
        driverLayout.addWidget(self.seatsText, 1, 0)
        driverLayout.addWidget(self.seats, 1, 1)
        driverLayout.addWidget(self.dateAndTimeText, 2, 0)
        driverLayout.addWidget(self.dateTime, 2, 1)
        driverLayout.addWidget(self.durationText, 2, 2)
        driverLayout.addWidget(self.durationEdit, 2, 3)
        self.generalLayout.addLayout(driverLayout)

        #Publish ride button#
        self.ridePub = QVBoxLayout()
        self.ridePubBttn=QPushButton("Publish ride offer!")
        self.ridePubBttn.setFont(QFont('Arial',10))
        self.ridePubBttn.clicked.connect(self.ridePubFunc)
        self.ridePub.addWidget(self.ridePubBttn)
        self.generalLayout.addLayout(self.ridePub)

########################Passenger ride settings#########################################

        #Request ride offer Title#
        self.requestRideOfferText=QLabel('Request ride offer:')
        self.requestRideOfferText.setFont(QFont('Arial',20))
        self.generalLayout.addWidget(self.requestRideOfferText)

        #Ride settings and filtering#
        filterLayout = QGridLayout()
        self.locationsFilterText=QLabel('Location:')
        self.locationsFilterText.setFont(QFont('Arial',15))
        self.dayText=QLabel('Day:')
        self.dayText.setFont(QFont('Arial',15))
        self.monthText=QLabel('Month:')
        self.monthText.setFont(QFont('Arial',15))
        self.locationsFilter=QComboBox()
        self.locationsFilter.addItems(["Coyoacan","Tlalpan","BenitoJuarez","Tlahuac","Iztapalapa"])
        self.months=QComboBox()
        self.months.addItems(["January","February","March","April","May","June","July","August","September","October","November","December"])
        self.dayEdit=QLineEdit("")
        filterLayout.addWidget(self.locationsFilterText, 0, 0)
        filterLayout.addWidget(self.locationsFilter, 0, 1)
        filterLayout.addWidget(self.monthText, 0, 2)
        filterLayout.addWidget(self.months, 0, 3)
        filterLayout.addWidget(self.dayText, 0, 4)
        filterLayout.addWidget(self.dayEdit, 0, 5)
        self.generalLayout.addLayout(filterLayout)

        #Ride selection and bid#
        passengerLayout = QGridLayout()
        self.rideOffers=QComboBox()
        self.rideOffers.addItems([])
        self.offersText=QLabel('Offers:')
        self.offersText.setFont(QFont('Arial',15))
        self.bidsText=QLabel('Bid:')
        self.bidsText.setFont(QFont('Arial',15))
        self.bidOffer=QLineEdit("")
        passengerLayout.addWidget(self.offersText, 0, 0)
        passengerLayout.addWidget(self.rideOffers, 0, 1)
        passengerLayout.addWidget(self.bidsText, 1, 0)
        passengerLayout.addWidget(self.bidOffer, 1, 1)
        self.generalLayout.addLayout(passengerLayout)        

        #Filter ride offer button#
        self.refreshRideOffersBttn=QPushButton('Filter ride offers!')
        self.refreshRideOffersBttn.setFont(QFont('Arial',10))
        self.refreshRideOffersBttn.clicked.connect(self.filterRideOffersFunc)
        self.generalLayout.addWidget(self.refreshRideOffersBttn)

        #Request bid offer button#
        self.bidPubBttn=QPushButton('Publish bid offer!')
        self.bidPubBttn.setFont(QFont('Arial',10))
        self.bidPubBttn.clicked.connect(self.bidPubFunc)
        self.generalLayout.addWidget(self.bidPubBttn)
#####################Passenger future travels#########################################################################################

        #My future travel Title#
        self.myFutureTravelsText=QLabel('My future travels:')
        self.myFutureTravelsText.setFont(QFont('Arial',20))
        self.generalLayout.addWidget(self.myFutureTravelsText)

        #My future travel display#
        self.myFutureTravels=QComboBox()
        self.myFutureTravels.addItems([])
        # Set some display's properties
        self.myFutureTravels.setFixedHeight(25)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.myFutureTravels)


        #Refresh my future travels button#
        self.myFutureTravelsBttn=QPushButton('Refresh travels!')
        self.myFutureTravelsBttn.setFont(QFont('Arial',10))
        self.myFutureTravelsBttn.clicked.connect(self.myFutureTravelsFunc)
        self.generalLayout.addWidget(self.myFutureTravelsBttn)

        #Display
        self.display=QLineEdit()
        self.display.setFixedHeight(20)
        self.generalLayout.addWidget(self.display)
#############################################################################################################################################
    #Driver login button function#
    def driverLoginFunc(self):
        driverAddress=self.driverAddressEdit.text()
        driverKey=self.driverKeyEdit.text()
        self.driverAddressEdit.clear()
        self.driverKeyEdit.clear()
        self.display.setText("Driver credentials registered")


    #Passenger login button function#
    def passengerLoginFunc(self):
        passengerAddress=self.passengerAddressEdit.text()
        passengerKey=self.passengerKeyEdit.text()
        self.passengerAddressEdit.clear()
        self.passengerKeyEdit.clear()
        self.display.setText("Passenger credentials registered")

    #Publish ride offer button function#
    def ridePubFunc(self):

        #get ride parameters's text
        currentPrice=self.priceEdit.text()
        currentLocation=self.locations.currentText()
        currentSeats=self.seats.currentText()
        currentDateAndTime=self.dateTime.text()
        currentDuration=self.durationEdit.text()

        if(currentPrice==""):#Check if price is empty
            self.display.setText("Please enter the price")
        elif(currentDuration==""):
            self.display.setText("Please enter the duration in minutes")
        elif(driverAddress==""): #Check if there is a driver Address
            self.display.setText("Dear driver, please login")
        else:
            rideTime = datetime.strptime(currentDateAndTime.replace('. ', '').replace('.', ''), '%d/%m/%Y %I:%M %p')#Convert string type to datetime type 
            biddingTime=(rideTime-datetime.now()).total_seconds()#-10*60 #Calculate available bidding time in seconds
            print(biddingTime)
            if(biddingTime>0): #Check if bidding time is positive    
                i = 0
                overlapping=False
                while i <= web3.eth.block_number:#Check for all blocks
                    block = web3.eth.get_block(i) #current block
                    for tx_hash in block['transactions']:
                        if(web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress!=None):#Check if the block has a contract address
                            tx= web3.eth.get_transaction(tx_hash)
                            if(tx['from']==driverAddress):#Check if the contract was created by the logged driver
                                contractExtracted = web3.eth.contract(
                                     address=web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress,
                                     abi=abi
                                )
                                basePriceDurationAndSeats=contractExtracted.functions.basePriceDurationAndSeats().call()
                                dateAndLocation=contractExtracted.functions.dateAndLocation().call()
                                try:
                                    basePriceDurationAndSeats=contractExtracted.functions.basePriceDurationAndSeats().call()#Obtain base price, duration and seats in a list from contract
                                    dateAndLocation=contractExtracted.functions.dateAndLocation().call()#Obtain dateTime and location in a list from contract
                                    t1_start=datetime.strptime(dateAndLocation[0].replace('. ', '').replace('.', ''), '%d/%m/%Y %I:%M %p')#Start time of ride from contract#
                                    t1_end=t1_start+timedelta(minutes=int(basePriceDurationAndSeats[1])) #End time of ride from contract
                                    t2_start=rideTime#Start time of ride from settings
                                    t2_end=t2_start+timedelta(minutes=int(currentDuration))#End time of ride from settings

                                    #Check if there is overlapping of time#                                    
                                    if((t2_start<t1_start and t2_end>t1_start) or (t2_start>=t1_start and t2_start<t1_end)):
                                        overlapping=True
                                        pass    
                                except:
                                    pass
                    i += 1
                if(overlapping==False):
                    print("Overlapping false")
                    #Creating contract
                    #Add the offer for the passenger and create the contract
                    self.rideOffers.addItems(["$: "+str(currentPrice)+"||"+str(currentLocation)+"||Seats: "+str(currentSeats)+"||"+str(currentDateAndTime)+"||minutes: "+str(currentDuration)])
                    self.contractCreate(driverAddress,currentPrice,currentSeats,currentDateAndTime, currentLocation,currentDuration,biddingTime)
                else:
                    self.display.setText("There is overlap of time")
                    
            else:
                self.display.setText("Error, you need a further traveling time")

    #Filter ride offers button#
    def filterRideOffersFunc(self):
        i = 0
        self.rideOffers.clear()
        self.rideOffers.addItems([""])
        while i <= web3.eth.block_number:

            block = web3.eth.get_block(i) # example for a recent block
            for tx_hash in block['transactions']:       
                if(web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress!=None):#Check if the block has contract address
                    contractExtracted = web3.eth.contract(
                         address=web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress,
                         abi=abi
                    )
                    try:
                        basePriceDurationAndSeats=contractExtracted.functions.basePriceDurationAndSeats().call()#Obtain base price, duration and seats in a list from contract
                        dateAndLocation=contractExtracted.functions.dateAndLocation().call()#Obtain dateTime and location in a list from contract
                        expiredStatus=contractExtracted.functions.contractExpiredStatus().call()#Obtain expired status

                        locationFilter=self.locationsFilter.currentText()##Obtain location from settings
                        monthFilter=self.months.currentText()#Obtain month from settings
                        dayEditFilter=self.dayEdit.text() #Obtain day from settings
                        months=months_in_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                        month=months[int(dateAndLocation[0][3:5])-1]#Obtain month from contract
                    
                        if(locationFilter==dateAndLocation[1] and monthFilter==month  and expiredStatus==False):#Check if location from settings and contract are equal
                            if(dayEditFilter==""):#Check if the user wants to filter by day or not
                                self.rideOffers.addItems(["$: "+str(basePriceDurationAndSeats[0])+"||"+str(dateAndLocation[0])+"||Seats: "+str(basePriceDurationAndSeats[2])+"||"+str(dateAndLocation[1])+"||minutes: "+str(basePriceDurationAndSeats[1])])
                            elif(int(dayEditFilter)==int(dateAndLocation[0][0:2])):
                                self.rideOffers.addItems(["$: "+str(basePriceDurationAndSeats[0])+"||"+str(dateAndLocation[0])+"||Seats: "+str(basePriceDurationAndSeats[2])+"||"+str(dateAndLocation[1])+"||minutes: "+str(basePriceDurationAndSeats[1])])
                    except:
                        pass
            i += 1
        self.display.setText("Ride Offers Refreshed")
 
    #Publish bid offer button#               
    def bidPubFunc(self):
        if(self.bidOffer.text()==""):#Check if there is a bid entered
            self.display.setText("Please enter bid")
        elif(self.rideOffers.currentText()==""):#Check if a ride offer is selected
            self.display.setText("Please select driver offer")
        else:
            currentRideOffer=self.rideOffers.currentText()#Obtain ride offer selected
            currentBid=self.bidOffer.text()#Obtain bid offer from passenger
            i = 0
            while i <= web3.eth.block_number:
                block = web3.eth.get_block(i) # example for a recent block
                for tx_hash in block['transactions']:
                    if(web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress!=None):#Check if the block has contract address
                        contractExtracted = web3.eth.contract(
                             address=web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress,
                             abi=abi
                        )
                        try:
                            contractExpiredStatus=contractExtracted.functions.contractExpiredStatus().call()
                            if(contractExpiredStatus==False):#Check if the contract has expired
                                basePriceDurationAndSeats=contractExtracted.functions.basePriceDurationAndSeats().call()#Obtain base price, duration and seats in a list from contract
                                dateAndLocation=contractExtracted.functions.dateAndLocation().call()#Obtain dateTime and location in a list from contract
                                currentRideOffer=self.rideOffers.currentText().split("||")#Make a list of all parameters from the ride option selected#
                                basePrice=currentRideOffer[0][2:]
                                dateAndTime=currentRideOffer[3]
                                seats=currentRideOffer[2][7:]
                                location=currentRideOffer[1]
                                duration=currentRideOffer[4][9:]
                                #print(basePrice)
                                #print(basePriceDurationAndSeats[0])
                                #print(basePriceDurationAndSeats[0]==basePrice)
                                #print(duration)
                                #print(basePriceDurationAndSeats[1])
                                #print(duration==basePriceDurationAndSeats[1])
                                #print(seats)
                                #print(basePriceDurationAndSeats[2])
                                #print(seats=basePriceDurationAndSeats[2])
                                print(dateAndTime)
                                print(dateAndLocation[0])
                                print(dateAndTime==dateAndLocation[0])
                                print(location)
                                print(dateAndLocation[1])
                                print(location==dateAndLocation[1])
                                #Check if the option selected matches the contract created#
                                if(int(basePrice)==int(basePriceDurationAndSeats[0]) and int(duration)==int(basePriceDurationAndSeats[1]) and int(seats)==(basePriceDurationAndSeats[2]) and dateAndTime==dateAndLocation[0] and location==dateAndLocation[1]):
                                    print("qwqw2")
                                    passanger_balance=int(web3.fromWei(web3.eth.get_balance(passengerAddress), 'ether'))
                                    basePrice=basePriceDurationAndSeats[0]
                                    if(passanger_balance>=basePrice):#Check if the passenger has enough balance for the price
                                        try:
                                            print("qwqw3")
                                            contractExtracted.functions.bid(passanger_balance,passengerAddress,int(currentBid)).transact()
                                            #self.futureTravels.setText(currentRideOffer+"✅")
                                            self.display.setText("Bid published")
                                        except:
                                            self.display.setText("Either the contract has expired or you don't have sufficient funds")
                        except:
                            pass
                
                
                i += 1
        
    def contractCreate(self,driver_address, basePrice, seats, dateAndTime, location, duration, biddingTime):
        web3.eth.defaultAccount=driver_address
        
        simpleAuction = web3.eth.contract(abi=abi, bytecode=bytecode)# Submit the transaction that deploys the contract
        tx_hash = simpleAuction.constructor(driver_address, int(basePrice), int(seats), str(dateAndTime), location, int(duration), int(biddingTime),str(abi)).transact()
        #print(web3.toHex(tx_hash))
        
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)# Wait for the transaction to be mined, and get the transaction receipt
        contractPublished = web3.eth.contract(
             address=tx_receipt.contractAddress,
             abi=abi
         )
        try:
            print(contractPublished.functions.dateAndLocation().call())
        except:
          pass
        self.display.setText("Contract created")

    #Passenger login button function#
    def myFutureTravelsFunc(self):
        i = 0
        while i <= web3.eth.block_number: #Check all blocks
            block = web3.eth.get_block(i) #Current block
            for tx_hash in block['transactions']:
                tx = web3.eth.get_transaction(tx_hash)
                tx_obj = {'addr_sender': tx['from'], 'addr_receiver': tx['to'], 'value': tx['value']}
                if(web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress!=None):#Check if there is a contract address for the block
                    contractExtracted = web3.eth.contract(
                         address=web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress, #Contract Address
                         abi=abi
                    )
                    try:
                        
                        contractStatus=contractExtracted.functions.contractExpiredStatus().call()
                        
                        highestBidder=contractExtracted.functions.highestBidder().call()
                        highestBid=contractExtracted.functions.highestBid().call()
                        print(highestBidder)
                        print(contractStatus)
                        print(highestBid)
                        if(True):#contractStatus==True and passengerAddress==highestBidder):##Check for contract status
                            basePriceDurationAndSeats=contractExtracted.functions.basePriceDurationAndSeats().call()#Obtain base price, duration and seats in a list from contract
                            dateAndLocation=contractExtracted.functions.dateAndLocation().call()#Obtain dateTime and location in a list from contract
                            self.myFutureTravels.addItems(["$: "+str(basePriceDurationAndSeats[0])+"||"+str(dateAndLocation[0])+"||Seats: "+str(basePriceDurationAndSeats[2])+"||"+str(dateAndLocation[1])+"||minutes: "+str(basePriceDurationAndSeats[1])])
                            
                    except:
                        pass
            i += 1
        #print("status checked")

def task2():
    print("Task 2 Running")
    while(True):
        i = 0
        while i <= web3.eth.block_number: #Check all blocks
            block = web3.eth.get_block(i) #Current block
            for tx_hash in block['transactions']:
                if(web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress!=None):#Check if there is a contract address for the block
                    contractExtracted = web3.eth.contract(
                         address=web3.eth.wait_for_transaction_receipt(tx_hash).contractAddress, #Contract Address
                         abi=abi
                    )
                    try:
                        contractStatus=contractExtracted.functions.contractExpiredStatus().call()
                        bidAmount=contractExtracted.functions.highestBidAmount().call()
                        if(contractStatus==False):##Check for contract status
                            nonce = web3.eth.getTransactionCount(passengerAddress)
                            contractExtracted.functions.auctionEnd().transact()
                            tx = {
                                'nonce': nonce,
                                'to': driverAddress,
                                'value': web3.toWei(bidAmount, 'ether'),  # One ether = 1,000,000,000,000,000,000 wei (10e18) 
                                'gas': 200000,  
                                'gasPrice': web3.toWei('3', 'gwei')
                            }
                            signed_tx = web3.eth.account.sign_transaction(tx, passengerKey)
                            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                            print("qwqwqwvvvvv")
                            
                            
                    except:
                        pass
            i += 1
        #print("status checked")

def task1():
    print("task 1 running")
    app = QApplication(sys.argv)
    view = CryptoProject()
    view.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    ganache_url = 'HTTP://127.0.0.1:8545'
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    print("Connection established: "+str(web3.isConnected()))

    driverAddress = '0xdedF15C43c695829b8136E078d650b3249891606'
    driverKey = 'df97b1dde60d9ce58cc35c67c0fbcd59a8c22fbf0140029c418a9ef825a02961'
        

    passengerAddress = '0xA908Fe1ED5114031CA015B1a3046E0618ace9b61'
    passengerKey = '30b52623db4f373275662eb0b5543b63ecabc687e551642c87c6f7ba6afb2adc'

    compiled_sol = compile_source(
        '''
        pragma solidity >=0.7.0 <0.9.0;

contract simpleAuction{
    //Parameter (do not change)
    address payable public beneficiary;
    uint public auctionEndTime;
    uint public basePrice;
    uint public seats;
    string public dateAndTime;
    string public location;   
    uint public duration;
    
    //Current state of the auction
    address[10] bidders;
    uint[10] public bids;
    mapping(address => uint) public pendingReturns;
    bool public ended = false;
    uint endedInt=0;
    uint i = 0;
    uint public highestBid = 0;
    address public highestBidder;
    event highestBidIncrease(address bidder, uint amount);
    event auctionEnded(address winner, uint amount);
    event addressAndAbi(address winner, string abi);
    event fundInsufficient(uint basePrice, uint account_balance);
    //event seats(uint seats);

    constructor(address payable _beneficiary, uint _basePrice, uint _seats, string memory _dateAndTime, string memory _location, uint _duration, uint _biddingTime, string memory _abi){
        beneficiary = _beneficiary;
        basePrice = _basePrice;
        dateAndTime = _dateAndTime;
        location = _location;
        duration = _duration;
        seats = _seats;
        emit addressAndAbi(msg.sender, _abi);
        auctionEndTime = block.timestamp + _biddingTime;

    }
    
    function bid (uint _account_balance, address _bidder, uint _amount) public{
        if (block.timestamp > auctionEndTime){
            //revert("Auction has already ended");
        }
        if (_account_balance< basePrice){
            //revert("You don't have sufficient funds to carry out the reservation");
            //emit fundInsufficient(basePrice,_account_balance);
        }
        if (_amount <= bids[i]){
            //revert("There is a higher or equal bid");
        }
        if (bids[i] != 0){
            pendingReturns[bidders[i]] += bids[i];
            
        }
        bidders[i] = _bidder;
        bids[i] = _amount;
        i++;
        emit highestBidIncrease(_bidder, _amount);
    }
    function auctionEnd()public {
        if (block.timestamp < auctionEndTime){
            revert("Auction has not ended yet");
        }
        if (ended){
            revert("Function auctionEnded has already been called");
        }
        ended = true;
        uint j;
        for(j=0;j<10;j++){
           if(highestBid<bids[j]){
               highestBid = bids[j];
               highestBidder = bidders[j];
           }
       }
        emit auctionEnded(highestBidder, highestBid);
        //beneficiary.transfer(highestBid);
        // send will returns false if it fails and transfer does not do anything, the code will stop there (throw)
    }
    function dateAndLocation() view public returns (string[2] memory) {
             return [dateAndTime, location];
    }
     function basePriceDurationAndSeats() view public returns (uint[3] memory) {
             return [basePrice,duration,seats];
             
    }
    function beneficiaryAddress() view public returns (address _beneficiary) {
             return beneficiary;
    }
    function contractExpiredStatus() view public returns (bool _ended) {
            _ended=ended;
             return _ended;
    }
    function highestBidderAddress() view public returns (address _highestBidder) {
            _highestBidder=highestBidder;
             return highestBidder;
    }
    function highestBidAmount() view public returns (uint _highestBidAmount) {
             return highestBid;
    }
}
             ''',
             output_values=['abi', 'bin']
        )
        
    # retrieve the contract interface
    contract_id, contract_interface = compiled_sol.popitem()

    # get bytecode / bin
    bytecode = contract_interface['bin']

    # get abi
    abi = contract_interface['abi']
    
    t1 = threading.Thread(target=task1, name='t1')
    t2=threading.Thread(target=task2,name='t2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
