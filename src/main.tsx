import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';
import './presentation/battle.css';
import './presentation/visual-game.css';
import './presentation/progress.css';
createRoot(document.getElementById('root')!).render(<App/>);
if(import.meta.env.PROD&&'serviceWorker' in navigator)window.addEventListener('load',()=>{void navigator.serviceWorker.register(`${import.meta.env.BASE_URL}sw.js`).catch(()=>undefined);});
