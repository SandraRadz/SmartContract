pragma solidity >=0.4.22 <0.9.0;

contract Escrow {
    uint public reward;
    uint public value;
    uint public description;
    
    address payable public seller;
    address payable public buyer;
    address payable public solver;
    address payable public admin;
    
    string public problem_description;
    string public item;
    
    enum State { Created, Locked, Troubled, Inactive }
    State public state;

    constructor(address payable _seller, address payable _solver, string memory item_id) public payable {
        item = item_id;
        seller = _seller;
        solver = _solver; 
        admin = address(0xD36549D00D81F35f7e44d48A46A966616fB2f945);
        value = msg.value;
        buyer = msg.sender;
        reward = msg.value / 50;
        admin.call.value(reward / 2);
    }
    
    modifier onlyBuyer() {
        require(msg.sender == buyer);
        _;
    }

    modifier onlySeller() {
        require(msg.sender == seller);
        _;
    }
    
    modifier onlySolver() {
        require(msg.sender == solver);
        _;
    }

    modifier inState(State _state) {
        require(state == _state);
        _;
    }
    
    event Aborted();
    event PurchaseConfirmed();
    event ItemReceived();
    event Sent();
    event ItemNotOk();
    event Refund();

    // Abort the purchase and reclaim the ether.
    // Can only be called by the seller before
    // the contract is locked.
    function abort()
        public
        onlyBuyer
        inState(State.Created)
    {
        emit Aborted();
        state = State.Inactive;
        buyer.call.value(address(this).balance);
    }
    
    // Confirm that the seller have sent the item.
    // This will lock ether.
    function sent()
        public
        onlySeller
        inState(State.Created)
    {
        emit Sent();
        state = State.Locked;
    }
    
    // Confirm that the buyer received the item.
    // This will release the locked ether.
    function confirmReceived()
        public
        onlyBuyer
        inState(State.Locked)
    {
        emit ItemReceived();
        // It is important to change the state first because
        // otherwise, the contracts called using `send` below
        // can call in again here.
        state = State.Inactive;

        // NOTE: This actually allows both the buyer and the seller to
        // block the refund - the withdraw pattern should be used.
        seller.transfer(address(this).balance);
    }
    
    // The buyer can print description of a problem with the item
    // in order to solver to see it and make a decision whether
    // the refund should be payed or not.
    function problem(string memory _problem_description)
        public
        onlyBuyer
        inState(State.Locked)
    {    
        emit ItemNotOk();
        problem_description = _problem_description;
        state = State.Troubled;
    }
    
    // Solver can return the transfer back to the buyer.
    function refund()
        public
        onlySolver
        inState(State.Troubled)
    {    
        emit Refund();
        state = State.Inactive;
        solver.transfer(reward);
        buyer.transfer(address(this).balance);
    }
    
    // Solver can transfer the payment to the seller.
    function no_refund()
        public
        onlySolver
        inState(State.Troubled)
    {    
        emit ItemReceived();
        state = State.Inactive;
        solver.transfer(reward);
        seller.transfer(address(this).balance);
    }
}