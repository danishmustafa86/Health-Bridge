import React, { useState } from 'react';
import { Calendar, Clock, User, CreditCard, CheckCircle } from 'lucide-react';
import { toast } from '../ui/toast';

const doctors = [
  { id: '1', name: 'Dr. Sarah Wilson', specialty: 'Cardiology', rating: 4.9, fee: 150 },
  { id: '2', name: 'Dr. Michael Chen', specialty: 'Neurology', rating: 4.8, fee: 180 },
  { id: '3', name: 'Dr. Emily Rodriguez', specialty: 'Dermatology', rating: 4.7, fee: 120 },
  { id: '4', name: 'Dr. David Kim', specialty: 'Orthopedics', rating: 4.9, fee: 200 },
];

const timeSlots = [
  '09:00 AM', '09:30 AM', '10:00 AM', '10:30 AM',
  '02:00 PM', '02:30 PM', '03:00 PM', '03:30 PM',
  '04:00 PM', '04:30 PM', '05:00 PM', '05:30 PM'
];

export default function AppointmentBooking() {
  const [selectedDoctor, setSelectedDoctor] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [showPayment, setShowPayment] = useState(false);
  const [paymentComplete, setPaymentComplete] = useState(false);

  const handleBookAppointment = () => {
    if (!selectedDoctor || !selectedDate || !selectedTime) {
      toast.error('Please fill in all required fields');
      return;
    }
    setShowPayment(true);
  };

  const handlePayment = () => {
    // Simulate payment processing
    setTimeout(() => {
      setPaymentComplete(true);
      toast.success('Appointment booked successfully!');
    }, 2000);
  };

  const selectedDoctorData = doctors.find(d => d.id === selectedDoctor);

  if (paymentComplete) {
    return (
      <div className="p-8">
        <div className="max-w-2xl mx-auto text-center">
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-6" />
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Appointment Confirmed!</h1>
          <p className="text-gray-600 mb-6">
            Your appointment has been successfully booked and confirmed.
          </p>
          <div className="bg-green-50 rounded-lg p-6 mb-6">
            <h3 className="font-semibold text-green-800 mb-2">Appointment Details</h3>
            <div className="text-sm text-green-700 space-y-1">
              <p><strong>Doctor:</strong> {selectedDoctorData?.name}</p>
              <p><strong>Date:</strong> {selectedDate}</p>
              <p><strong>Time:</strong> {selectedTime}</p>
              <p><strong>Fee:</strong> ${selectedDoctorData?.fee}</p>
            </div>
          </div>
          <button
            onClick={() => {
              setSelectedDoctor('');
              setSelectedDate('');
              setSelectedTime('');
              setShowPayment(false);
              setPaymentComplete(false);
            }}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Book Another Appointment
          </button>
        </div>
      </div>
    );
  }

  if (showPayment) {
    return (
      <div className="p-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Payment Details</h1>
          
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 mb-6">
            <h3 className="font-semibold text-gray-900 mb-4">Appointment Summary</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Doctor:</span>
                <span className="font-medium">{selectedDoctorData?.name}</span>
              </div>
              <div className="flex justify-between">
                <span>Date:</span>
                <span className="font-medium">{selectedDate}</span>
              </div>
              <div className="flex justify-between">
                <span>Time:</span>
                <span className="font-medium">{selectedTime}</span>
              </div>
              <div className="flex justify-between border-t pt-2">
                <span className="font-semibold">Total:</span>
                <span className="font-bold">${selectedDoctorData?.fee}</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
              <CreditCard className="w-5 h-5 mr-2" />
              Payment Method
            </h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Card Number
                </label>
                <input
                  type="text"
                  placeholder="1234 5678 9012 3456"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Expiry Date
                  </label>
                  <input
                    type="text"
                    placeholder="MM/YY"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    CVV
                  </label>
                  <input
                    type="text"
                    placeholder="123"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={() => setShowPayment(false)}
                  className="flex-1 bg-gray-200 text-gray-800 py-3 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Back
                </button>
                <button
                  onClick={handlePayment}
                  className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Pay ${selectedDoctorData?.fee}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Book Appointment</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Doctor Selection */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
              <User className="w-5 h-5 mr-2" />
              Select Doctor
            </h2>
            <div className="space-y-3">
              {doctors.map((doctor) => (
                <label
                  key={doctor.id}
                  className={`block p-4 rounded-lg border-2 cursor-pointer transition-colors ${
                    selectedDoctor === doctor.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <input
                    type="radio"
                    name="doctor"
                    value={doctor.id}
                    checked={selectedDoctor === doctor.id}
                    onChange={(e) => setSelectedDoctor(e.target.value)}
                    className="sr-only"
                  />
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold text-gray-900">{doctor.name}</h3>
                      <p className="text-sm text-gray-600">{doctor.specialty}</p>
                      <div className="flex items-center mt-1">
                        <span className="text-yellow-500">★</span>
                        <span className="text-sm text-gray-600 ml-1">{doctor.rating}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">${doctor.fee}</p>
                      <p className="text-sm text-gray-600">per visit</p>
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Date and Time Selection */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Calendar className="w-5 h-5 mr-2" />
                Select Date
              </h2>
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <Clock className="w-5 h-5 mr-2" />
                Select Time
              </h2>
              <div className="grid grid-cols-3 gap-3">
                {timeSlots.map((time) => (
                  <button
                    key={time}
                    onClick={() => setSelectedTime(time)}
                    className={`p-3 rounded-lg border-2 text-sm font-medium transition-colors ${
                      selectedTime === time
                        ? 'border-blue-500 bg-blue-50 text-blue-700'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    {time}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleBookAppointment}
              disabled={!selectedDoctor || !selectedDate || !selectedTime}
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Book Appointment
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}