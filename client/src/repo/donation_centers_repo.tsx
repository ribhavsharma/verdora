interface DonationCenter {
    name: string;
    link: string; 
    address: string; 
    contact: string; 
}
const DonationCentersRepo: Record<string, DonationCenter[]> = {
    clothes: [
      {
        name: "Salvation Army",
        link: "kelownasalvationarmy.ca",
        address: "1480 Sutherland Ave, Kelowna, BC, V1Y 5Y5",
        contact: "250.860.2329",
      },
      {
        name: "Value Village",
        link: "https://stores.savers.com/bc/kelowna/",
        address: "190 Aurora Crescent Kelowna, BC V1X 7M3",
        contact: "250.491.1356",
      },
    ],
    eWaste: [
      {
        name: "Battery Doctors",
        link: "https://www.thebatterydrs.com/",
        address: "1972 Windsor Road Kelowna, British Columbia V1Y 4R5",
        contact: "250.860.2866",
      },
      {
        name: "Quantum Lifecycle",
        link: "https://quantumlifecycle.com/",
        address: "460 Doyle Avenue Kelowna, BC V1Y 2A2",
        contact: "416.222.1773",
      },
    ],
};
  
  export default DonationCentersRepo;
  