#include <iostream>
#include <thread>
#include <vector>
#include <mutex>
#include <chrono>
#include <string>
#include <ctime>

//constant for whole programm
int TOTAL_TICKETS = 250;
using namespace std;
mutex ticket_mutex;

//struct of thread
struct ThreadData {
    int id;
    string movie_title;
	string date_time;
};

//function for running the thread
void SellTickets(ThreadData data) {
	//prinitng while starting the thread
    cout << "Seller " << data.id << " started a movie : " << data.movie_title << " at " << data.date_time << endl;

    while(true) {
		//getting current time adn date
        ticket_mutex.lock();
		
		time_t now = time(0);
		string dt =ctime(&now);
		dt.pop_back();
		
		data.date_time = dt;

        if (TOTAL_TICKETS <= 0) {
            ticket_mutex.unlock();
            break;
        }

        TOTAL_TICKETS--;
		//selling the ticket
        cout << "Seller " << data.id << " sold a ticket.  Remaining : " << TOTAL_TICKETS << " time check " << data.date_time<<endl;

        this_thread::sleep_for(chrono::milliseconds(25));

        ticket_mutex.unlock();
    }
}

int main() { 
    const int num_threads = 6;
    vector<thread> threads;
	
	string title[6] = {"Star Wars", "Barbie", "Openheimer", "Car 1", "Car 2", "Car 3"};

    auto start_time = chrono::high_resolution_clock::now();

    for (int i = 0; i < num_threads; ++i){
		//getting current time adn date
		time_t now = time(0);
		string dt =ctime(&now);
		dt.pop_back();
		
		
        ThreadData data = {i + 1, title[i], dt}; 
        
        threads.push_back(thread(SellTickets, data));
    }

    for (auto& th : threads){
        th.join();
    }
	
	//claculating the time of running the porgramm

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end_time - start_time;

    cout << "\nAll Tickets sold" << endl;
    cout << "Execution time : " << elapsed.count() << " sec" << endl;
	
    return 0; 
}