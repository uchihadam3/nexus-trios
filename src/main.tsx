import { createRoot } from 'react-dom/client';
import App from './App';
import './styles.css';
import './presentation/battle.css';
import './presentation/visual-game.css';
import './presentation/arena.css';
import './presentation/acting-motion.css';
import './presentation/acting.css';
import './presentation/vfx-families.css';
import './presentation/progress.css';
import './presentation/identity-card.css';
import './presentation/ui-fx.css';
import './presentation/result-v2.css';
import './presentation/home-v2.css';
import './presentation/draft-v2.css';
import './presentation/roster-v2.css';
import './presentation/ficha-v2.css';
import './presentation/casca-v2.css';
import './presentation/telas-v2.css';
createRoot(document.getElementById('root')!).render(<App/>);
/*
 * Versão nova do jogo. O service worker novo assume na hora (skipWaiting), mas
 * a aba aberta continua rodando o código velho até recarregar — e uma jornada
 * jogada nele não entra no ranking (o servidor só aceita a versão atual). Ao
 * voltar para a aba, o jogo procura atualização; quando a versão nova assume,
 * o App mostra "Nova versão · Atualizar".
 */
if(import.meta.env.PROD&&'serviceWorker' in navigator)window.addEventListener('load',()=>{
  const tinha=!!navigator.serviceWorker.controller;
  navigator.serviceWorker.addEventListener('controllerchange',()=>{if(tinha)window.dispatchEvent(new Event('nexus:versao-nova'));});
  void navigator.serviceWorker.register(`${import.meta.env.BASE_URL}sw.js`).then(reg=>{
    document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible')void reg.update().catch(()=>undefined);});
    setInterval(()=>void reg.update().catch(()=>undefined),30*60*1000);
  }).catch(()=>undefined);
});
