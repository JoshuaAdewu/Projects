// CMSC 341 - Fall 2020 - Project 3
// PQueue: an ER triage queue using a skew heap and function pointers

#include "pqueue.h"
using namespace std;
using std::cout;
using std::endl;
using std::domain_error;

PQueue::PQueue(prifn_t priFn) {
  priority = priFn;
  _heap = nullptr;
  _size = 0;
}

PQueue::~PQueue() {
  nPatients(_heap);
}

Node* PQueue::cpyHlpr(Node* rhs){
  if(rhs == nullptr)
    return nullptr;

  Node *cpyNode = new Node(rhs -> _patient);
  cpyNode-> _left = cpyHlpr(rhs -> _left);
  cpyNode -> _right = cpyHlpr(rhs -> _right);
  return cpyNode;
}


PQueue::PQueue(const PQueue& rhs) {
  _heap = nullptr;
  _heap = cpyHlpr(rhs._heap);
  _size = rhs._size;
  priority = rhs.priority;
}


PQueue& PQueue::operator=(const PQueue& rhs) {
  if(this != &rhs){
    nPatients(_heap);
    _heap = cpyHlpr(rhs._heap);
    _size = rhs._size;
    priority = rhs.priority;
  }
  return *this;
}

void PQueue::insertPatient(const Patient& input) {
  
  Node *newNode = new Node(input); 
  _heap = mergeHlpr(_heap, newNode);
  _size++;
}

Patient PQueue::getNextPatient() {
  Patient nextP;
  Node *newL = _heap -> _left;
  Node *newR = _heap ->_right;
  if(_heap == nullptr){
    throw domain_error("queue is empty!");
  }
  
  nextP = _heap -> _patient;
  delete _heap;
  _size--;
  _heap = mergeHlpr(newL, newR);
  return nextP;
  
}

Node* PQueue::mergeHlpr(Node *fHeap, Node *sHeap){
  Node *p1;
  if(fHeap == nullptr){
    return sHeap;
  }

  if(sHeap == nullptr){
    return fHeap;
  }

  if(priority(fHeap -> _patient) < priority(sHeap ->_patient)){
    p1 = fHeap;
    fHeap = sHeap;
    sHeap = p1;
  }
  p1 = fHeap -> _right;
  fHeap -> _right = fHeap -> _left;
  fHeap -> _left = p1;
  fHeap -> _left = mergeHlpr(fHeap -> _left, sHeap);
  return fHeap;
  
}


void PQueue::mergeWithQueue(PQueue& rhs) {
  if(rhs._heap == nullptr){
    return;
  }
  if((_heap != rhs._heap) && (rhs.getPriorityFn() == this -> getPriorityFn())){
  _heap = mergeHlpr(_heap, rhs._heap);
  _size = _size + rhs.numPatients();
  rhs._heap = nullptr;
  }
  else{
    throw domain_error("cannot merge with different priority function");
  }
}

void PQueue::nPatients(Node* patient){
  if(patient != nullptr){
    if(patient -> _left != nullptr)
      nPatients(patient -> _left);
    if(patient -> _right != nullptr)
      nPatients(patient -> _right);
  }
  delete patient;
}


void PQueue::clear() {
  nPatients(_heap);
}

int PQueue::numPatients() const {
  return _size;
}

void PQueue::printPatientHlpr(Node *patient) const {
  if(patient == nullptr){
    return;
  }
  cout<< patient -> _patient << endl;
  printPatientHlpr(patient -> _left);
  printPatientHlpr(patient -> _right);
}


void PQueue::printPatientQueue() const {
  printPatientHlpr(_heap);
}

prifn_t PQueue::getPriorityFn() const {
  return priority;
}

void PQueue::setPriorityFn(prifn_t priFn) {
  Patient* array = new Patient[_size];
  int count = 0;
  int num = _size;

  while(count < num){
    array[count] = getNextPatient();
    count++;
  }
  priority = priFn;
  for(int i = 0; i < num; i++){
    insertPatient(array[i]);
  }
  
  delete []array;
}

void PQueue::dumpHlpr(Node* here) const{
  if(here == nullptr)
    return;
  cout<<"(";
  dumpHlpr(here -> _left);
  cout<< priority(here -> _patient);
  cout<< ":" << here -> getPatient().getPatient();
  dumpHlpr(here -> _right);
  cout<<")";
}


void PQueue::dump() const
{
  dumpHlpr(_heap);
}

ostream& operator<<(ostream& sout, const Patient& patient) {
  sout << "Patient: " << patient.getPatient() << ", triage: " << patient.getTriage()
       << ", temperature: " << patient.getTemperature() << ", oxygen: " << patient.getOxygen() << ", RR: "
       << patient.getRR() << ", HR: " << patient.getHR() << ", BP: " << patient.getBP();
  return sout;
}

ostream& operator<<(ostream& sout, const Node& node) {
  sout << node.getPatient();
  return sout;
}

