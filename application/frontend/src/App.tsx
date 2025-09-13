import { Route, Routes } from 'react-router-dom';
import {
  Analytics,
  ConsumerForm,
  Forecast,
  Home,
  NotFound,
  Profile,
  Survey,
} from './pages';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/contract" element={<ConsumerForm />} />
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/forecast" element={<Forecast />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/survey" element={<Survey />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
