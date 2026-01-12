export default function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <span className="text-2xl mr-2">📦</span>
            <span className="font-bold text-xl text-blue-600">GOMAHTECH Stock</span>
          </div>
          <div className="flex items-center space-x-4">
            <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
              A
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}