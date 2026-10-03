const assetPathPrefix = "../assets/figma";
const imgIconePlay = `${assetPathPrefix}/d69f1.svg`;
const imgIconeStop = `${assetPathPrefix}/186ba.svg`;
const imgIconePausa = `${assetPathPrefix}/cba5a.svg`;
const imgIconeProximo = `${assetPathPrefix}/3d8ce.svg`;
const imgPlayerTransport = `${assetPathPrefix}/bc380.svg`;
const imgVector = `${assetPathPrefix}/c9365.svg`;
const imgVector1 = `${assetPathPrefix}/aa062.svg`;
const imgVector2 = `${assetPathPrefix}/a0255.svg`;
const imgIconeControleDeNiveis = `${assetPathPrefix}/191cb.svg`;
const imgEllipse = `${assetPathPrefix}/61d97.svg`;
const imgAbrirPainel = `${assetPathPrefix}/0b259.svg`;
const imgIconSearch = `${assetPathPrefix}/a8263.svg`;
const imgToggleCollapsed = `${assetPathPrefix}/a95fb.svg`;
const imgIconCloud = `${assetPathPrefix}/2e02f.svg`;
const imgIconUser = `${assetPathPrefix}/f187e.svg`;
const imgToggleExpanded = `${assetPathPrefix}/f6a98.svg`;
const imgIconComputer = `${assetPathPrefix}/6b6ec.svg`;
const imgIconFolder = `${assetPathPrefix}/982f2.svg`;
const imgIconNetwork = `${assetPathPrefix}/ec847.svg`;
const imgPlayerPlaylist = `${assetPathPrefix}/0e84b.svg`;
const imgVector3 = `${assetPathPrefix}/55cee.svg`;
const imgVector4 = `${assetPathPrefix}/67bf5.svg`;
const imgVector5 = `${assetPathPrefix}/99e9b.svg`;
const imgVector6 = `${assetPathPrefix}/895dc.svg`;
const imgVector7 = `${assetPathPrefix}/f6246.svg`;
const imgVector8 = `${assetPathPrefix}/641d3.svg`;
const imgVector9 = `${assetPathPrefix}/aec68.svg`;
const imgVector10 = `${assetPathPrefix}/23fa6.svg`;
const imgVector11 = `${assetPathPrefix}/f5f84.svg`;
const imgVector12 = `${assetPathPrefix}/4cc7a.svg`;
const imgPlayerPlaybackModes = `${assetPathPrefix}/e50d5.svg`;
const imgVector13 = `${assetPathPrefix}/76a37.svg`;
const imgVector14 = `${assetPathPrefix}/50115.svg`;
const imgVector15 = `${assetPathPrefix}/c2dd3.svg`;
const imgVector16 = `${assetPathPrefix}/366b1.svg`;
const imgVector17 = `${assetPathPrefix}/d5471.svg`;
const imgVector18 = `${assetPathPrefix}/9ad05.svg`;
const imgVector19 = `${assetPathPrefix}/759d3.svg`;
const imgPlayerStudioClockMeters = `${assetPathPrefix}/6fa90.svg`;
const imgVector20 = `${assetPathPrefix}/654d1.svg`;
const imgVector21 = `${assetPathPrefix}/ea1ec.svg`;
const imgVector22 = `${assetPathPrefix}/f1ba9.svg`;
const imgVector23 = `${assetPathPrefix}/0b2f3.svg`;
const imgVector24 = `${assetPathPrefix}/e8a65.svg`;
const imgVector25 = `${assetPathPrefix}/27065.svg`;
const imgPlayerDeckNext = `${assetPathPrefix}/43bc0.svg`;
const imgVector26 = `${assetPathPrefix}/929c6.svg`;
const imgVector27 = `${assetPathPrefix}/c1208.svg`;
const imgVector28 = `${assetPathPrefix}/0b840.svg`;
const imgVector29 = `${assetPathPrefix}/561eb.svg`;
const imgVector30 = `${assetPathPrefix}/5a719.svg`;
const imgVector31 = `${assetPathPrefix}/83abe.svg`;
const imgVector32 = `${assetPathPrefix}/05300.svg`;
const imgVector33 = `${assetPathPrefix}/2d1a0.svg`;
const imgPlayerToolbar = `${assetPathPrefix}/27173.svg`;
const imgVector34 = `${assetPathPrefix}/f05b2.svg`;
const imgVector35 = `${assetPathPrefix}/a80c1.svg`;
const imgVector36 = `${assetPathPrefix}/10094.svg`;
const imgVector37 = `${assetPathPrefix}/89145.svg`;
const imgVector38 = `${assetPathPrefix}/f8d06.svg`;
const imgPlayerHeader = `${assetPathPrefix}/9f505.svg`;
const imgVector39 = `${assetPathPrefix}/f58b6.svg`;
const imgVector40 = `${assetPathPrefix}/9dd12.svg`;
const imgVector41 = `${assetPathPrefix}/862d9.svg`;
const imgVbcPlayerGruposEditaveis = `${assetPathPrefix}/1f628.svg`;
const imgVAzulMarinho = `${assetPathPrefix}/5979e.svg`;
const imgVCiano = `${assetPathPrefix}/a7a41.svg`;
const imgBAzul = `${assetPathPrefix}/77e34.svg`;
const imgBAzulMarinho = `${assetPathPrefix}/81850.svg`;
const imgCAzulMarinho = `${assetPathPrefix}/0b8f9.svg`;
const imgCCiano = `${assetPathPrefix}/03866.svg`;
const imgVector42 = `${assetPathPrefix}/6189b.svg`;

type PlayerBotoesDeTransporteProps = {
  className?: string;
  acao?: "Play" | "Stop" | "Pausa" | "Próximo";
  estado?: "Padrão";
};

function PlayerBotoesDeTransporte({ className, acao = "Play", estado = "Padrão" }: PlayerBotoesDeTransporteProps) {
  const isPausaAndPadrao = acao === "Pausa" && estado === "Padrão";
  const isPlayAndPadrao = acao === "Play" && estado === "Padrão";
  const isProximoAndPadrao = acao === "Próximo" && estado === "Padrão";
  const isStopAndPadrao = acao === "Stop" && estado === "Padrão";
  return (
    <div className={className || `border border-solid content-stretch flex gap-[12px] h-[60px] items-center justify-center relative rounded-[var(--vbc-agc-radius,12px)] ${isProximoAndPadrao ? "bg-[var(--vbc-transport-next,#162c50)] border-[var(--vbc-transport-next-border,#345c92)] w-[152px]" : isPausaAndPadrao ? "bg-[var(--vbc-agc-surface,#182335)] border-[var(--vbc-agc-border,#2b3b52)] w-[120px]" : isStopAndPadrao ? "bg-[var(--vbc-agc-surface,#182335)] border-[var(--vbc-agc-border,#2b3b52)] w-[112px]" : "bg-[var(--vbc-transport-play,#f5682d)] border-[var(--vbc-transport-play-border,#ff9968)] w-[172px]"}`} id={isProximoAndPadrao ? "node-52_150" : isPausaAndPadrao ? "node-52_144" : isStopAndPadrao ? "node-52_139" : "node-52_133"}>
      {isPlayAndPadrao && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="52:134" data-name="Ícone / Play">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconePlay} />
          </div>
          <div className="[word-break:break-word] content-stretch flex flex-col items-start leading-[1.4] not-italic overflow-clip relative shrink-0 text-[color:var(--vbc-agc-text,#f4f7fc)] whitespace-nowrap" data-node-id="52:136" data-name="Rótulo">
            <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[13px]" data-node-id="52:137">
              PLAY
            </p>
            <p className="font-['Inter:Medium'] font-medium opacity-78 relative shrink-0 text-[10px]" data-node-id="52:138">
              ESPAÇO
            </p>
          </div>
        </>
      )}
      {isStopAndPadrao && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="52:140" data-name="Ícone / Stop">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconeStop} />
          </div>
          <div className="content-stretch flex flex-col items-start overflow-clip relative shrink-0" data-node-id="52:142" data-name="Rótulo">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.4] not-italic relative shrink-0 text-[13px] text-[color:var(--vbc-agc-text,#f4f7fc)] whitespace-nowrap" data-node-id="52:143">
              STOP
            </p>
          </div>
        </>
      )}
      {isPausaAndPadrao && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="52:145" data-name="Ícone / Pausa">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconePausa} />
          </div>
          <div className="content-stretch flex flex-col items-start overflow-clip relative shrink-0" data-node-id="52:148" data-name="Rótulo">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.4] not-italic relative shrink-0 text-[13px] text-[color:var(--vbc-agc-text,#f4f7fc)] whitespace-nowrap" data-node-id="52:149">
              PAUSA
            </p>
          </div>
        </>
      )}
      {isProximoAndPadrao && (
        <>
          <div className="relative shrink-0 size-[24px]" data-node-id="52:151" data-name="Ícone / Próximo">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconeProximo} />
          </div>
          <div className="content-stretch flex flex-col items-start overflow-clip relative shrink-0" data-node-id="52:154" data-name="Rótulo">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.4] not-italic relative shrink-0 text-[13px] text-[color:var(--vbc-agc-text,#f4f7fc)] whitespace-nowrap" data-node-id="52:155">
              PRÓXIMO
            </p>
          </div>
        </>
      )}
    </div>
  );
}

function PlayerTransport({ className }: { className?: string }) {
  return (
    <div className={className || "h-[92px] relative w-[1404px]"} data-node-id="24:10" data-name="Player/Transport">
      <div className="absolute inset-[-0.54%_0]">
        <img alt="" className="block max-w-none size-full" src={imgPlayerTransport} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[20.65%_51.64%_67.39%_45.73%] leading-[normal] not-italic text-[#64748b] text-[9px] whitespace-nowrap" data-node-id="17:603">
        MASTER
      </p>
      <div className="absolute inset-[56.52%_32.91%_36.96%_45.73%]" data-node-id="17:604" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector} />
      </div>
      <div className="absolute inset-[56.52%_39.03%_36.96%_45.73%]" data-node-id="17:605" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector1} />
      </div>
      <div className="absolute bottom-[30.43%] left-[60.33%] right-[38.39%] top-1/2" data-node-id="17:606" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector2} />
      </div>
      <p className="[word-break:break-word] absolute font-['Arial:Regular'] inset-[51.09%_29.27%_33.7%_67.95%] leading-[normal] not-italic text-[#94a3b8] text-[12px] whitespace-nowrap" data-node-id="17:607">
        -4.2 dB
      </p>
      <button className="absolute bg-[var(--vbc-agc-buttonbackground,#113a32)] border border-[var(--vbc-agc-buttonaccent,#4ce0ae)] border-solid content-stretch cursor-pointer flex gap-[12px] h-[60px] items-center justify-center left-[1208px] rounded-[var(--vbc-agc-radius,12px)] top-[16px] w-[178px]" data-node-id="47:829" data-name="AGC / Abrir monitoramento">
        <div className="relative shrink-0 size-[24px]" data-node-id="I47:829;47:563" data-name="Ícone / controle de níveis">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconeControleDeNiveis} />
        </div>
        <div className="content-stretch flex flex-col gap-px items-center justify-center overflow-clip relative shrink-0" data-node-id="I47:829;47:565" data-name="Nome e estado">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.4] not-italic relative shrink-0 text-[16px] text-[color:var(--vbc-agc-text,#f4f7fc)] text-left whitespace-nowrap" data-node-id="I47:829;47:566">
            AGC
          </p>
          <div className="content-stretch flex gap-[var(--vbc-agc-gap,8px)] items-center overflow-clip relative shrink-0" data-node-id="I47:829;47:567" data-name="Estado">
            <div className="relative shrink-0 size-[5px]" data-node-id="I47:829;47:568" data-name="Ellipse">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgEllipse} />
            </div>
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.4] not-italic relative shrink-0 text-[11px] text-[color:var(--vbc-agc-buttonaccent,#4ce0ae)] text-left whitespace-nowrap" data-node-id="I47:829;47:569">
              Ligado
            </p>
          </div>
        </div>
        <div className="relative shrink-0 size-[16px]" data-node-id="I47:829;47:570" data-name="Abrir painel">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgAbrirPainel} />
        </div>
      </button>
      <div className="absolute content-stretch cursor-pointer flex gap-[12px] items-center left-[16px] overflow-clip top-[16px]" data-node-id="52:227" data-name="Player / Controles">
        <PlayerBotoesDeTransporte className="bg-[var(--vbc-transport-play,#f5682d)] border border-[var(--vbc-transport-play-border,#ff9968)] border-solid content-stretch flex gap-[12px] h-[60px] items-center justify-center relative rounded-[var(--vbc-agc-radius,12px)] shrink-0 w-[172px]" />
        <PlayerBotoesDeTransporte acao="Stop" className="bg-[var(--vbc-agc-surface,#182335)] border border-[var(--vbc-agc-border,#2b3b52)] border-solid content-stretch flex gap-[12px] h-[60px] items-center justify-center relative rounded-[var(--vbc-agc-radius,12px)] shrink-0 w-[112px]" />
        <PlayerBotoesDeTransporte acao="Pausa" className="bg-[var(--vbc-agc-surface,#182335)] border border-[var(--vbc-agc-border,#2b3b52)] border-solid content-stretch flex gap-[12px] h-[60px] items-center justify-center relative rounded-[var(--vbc-agc-radius,12px)] shrink-0 w-[120px]" />
        <PlayerBotoesDeTransporte acao="Próximo" className="bg-[var(--vbc-transport-next,#162c50)] border border-[var(--vbc-transport-next-border,#345c92)] border-solid content-stretch flex gap-[12px] h-[60px] items-center justify-center relative rounded-[var(--vbc-agc-radius,12px)] shrink-0 w-[152px]" />
      </div>
    </div>
  );
}

function PlayerFileExplorer({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[#111a2a] border border-[#26344a] border-solid content-stretch flex flex-col h-[400px] items-start overflow-clip relative rounded-[12px] w-[378px]"} data-node-id="24:9" data-name="Player/File Explorer">
      <div className="bg-[#121d2f] content-stretch flex h-[52px] items-center justify-between overflow-clip px-[18px] relative shrink-0 w-full" data-node-id="26:2" data-name="Header">
        <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[normal] not-italic relative shrink-0 text-[#f2f5fa] text-[13px] whitespace-nowrap" data-node-id="26:3">
          EXPLORADOR DE ÁUDIO
        </p>
        <div className="bg-[#1e2b40] content-stretch flex items-start overflow-clip px-[9px] py-[5px] relative rounded-[12px] shrink-0" data-node-id="26:4" data-name="Source badge">
          <p className="[word-break:break-word] font-['Inter:Bold'] font-bold leading-[normal] not-italic relative shrink-0 text-[#8ea0bb] text-[9px] whitespace-nowrap" data-node-id="26:5">
            LOCAL
          </p>
        </div>
      </div>
      <div className="bg-[#0f1827] content-stretch flex flex-col gap-[10px] h-[346px] items-start overflow-clip pb-[12px] pt-[14px] px-[18px] relative shrink-0 w-full" data-node-id="26:6" data-name="Explorer content">
        <div className="bg-[#162238] border border-[#2a3a54] border-solid content-stretch flex gap-[9px] h-[36px] items-center overflow-clip px-[12px] relative rounded-[7px] shrink-0 w-full" data-node-id="26:7" data-name="Search">
          <div className="relative shrink-0 size-[18px]" data-node-id="26:8" data-name="Icon/Search">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconSearch} />
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[normal] not-italic relative shrink-0 text-[#74839c] text-[11px] whitespace-nowrap" data-node-id="26:11">
            Buscar arquivos e pastas
          </p>
        </div>
        <div className="[word-break:break-word] content-stretch flex gap-[6px] h-[24px] items-center leading-[normal] not-italic overflow-clip relative shrink-0 text-[10px] w-full whitespace-nowrap" data-node-id="26:12" data-name="Breadcrumb">
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[#7f90aa]" data-node-id="26:13">
            Este computador
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[#4e607c]" data-node-id="26:14">
            /
          </p>
          <p className="font-['Inter:Bold'] font-bold relative shrink-0 text-[#b9c8dd]" data-node-id="26:15">
            Músicas
          </p>
        </div>
        <div className="bg-[#111c2d] border border-[#223149] border-solid content-stretch flex flex-col gap-[2px] h-[198px] items-start overflow-clip py-[2px] relative rounded-[7px] shrink-0 w-full" data-node-id="26:16" data-name="File tree">
          <div className="content-stretch flex gap-[7px] h-[26px] items-center overflow-clip px-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:17" data-name="Tree row / OneDrive">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:18" data-name="Toggle/Collapsed">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleCollapsed} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:20" data-name="Icon/cloud">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconCloud} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[normal] min-w-px not-italic relative text-[#c7d2e3] text-[11px]" data-node-id="26:23">
              OneDrive
            </p>
          </div>
          <div className="content-stretch flex gap-[7px] h-[26px] items-center overflow-clip px-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:24" data-name="Tree row / Nicolas">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:25" data-name="Toggle/Collapsed">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleCollapsed} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:27" data-name="Icon/user">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconUser} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[normal] min-w-px not-italic relative text-[#c7d2e3] text-[11px]" data-node-id="26:30">
              Nicolas
            </p>
          </div>
          <div className="content-stretch flex gap-[7px] h-[26px] items-center overflow-clip px-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:31" data-name="Tree row / Este computador">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:32" data-name="Toggle/Expanded">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleExpanded} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:34" data-name="Icon/computer">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconComputer} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[normal] min-w-px not-italic relative text-[#c7d2e3] text-[11px]" data-node-id="26:38">
              Este computador
            </p>
          </div>
          <div className="content-stretch flex gap-[7px] h-[26px] items-center overflow-clip pl-[28px] pr-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:39" data-name="Tree row / Bibliotecas">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:40" data-name="Toggle/Collapsed">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleCollapsed} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:42" data-name="Icon/folder">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconFolder} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[normal] min-w-px not-italic relative text-[#c7d2e3] text-[11px]" data-node-id="26:45">
              Bibliotecas
            </p>
          </div>
          <div className="bg-[#173a68] content-stretch flex gap-[7px] h-[26px] items-center overflow-clip pl-[28px] pr-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:46" data-name="Tree row / Músicas">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:47" data-name="Toggle/Expanded">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleExpanded} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:49" data-name="Icon/folder">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconFolder} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Bold'] font-bold leading-[normal] min-w-px not-italic relative text-[#f4f8ff] text-[11px]" data-node-id="26:52">
              Músicas
            </p>
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[normal] not-italic relative shrink-0 text-[#8cc6ff] text-[9px] whitespace-nowrap" data-node-id="26:53">
              24
            </p>
          </div>
          <div className="content-stretch flex gap-[7px] h-[26px] items-center overflow-clip pl-[28px] pr-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:54" data-name="Tree row / Downloads">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:55" data-name="Toggle/Collapsed">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleCollapsed} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:57" data-name="Icon/folder">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconFolder} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[normal] min-w-px not-italic relative text-[#c7d2e3] text-[11px]" data-node-id="26:60">
              Downloads
            </p>
          </div>
          <div className="content-stretch flex gap-[7px] h-[26px] items-center overflow-clip px-[10px] relative rounded-[5px] shrink-0 w-full" data-node-id="26:61" data-name="Tree row / Rede">
            <div className="relative shrink-0 size-[14px]" data-node-id="26:62" data-name="Toggle/Collapsed">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgToggleCollapsed} />
            </div>
            <div className="relative shrink-0 size-[18px]" data-node-id="26:64" data-name="Icon/network">
              <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgIconNetwork} />
            </div>
            <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[normal] min-w-px not-italic relative text-[#c7d2e3] text-[11px]" data-node-id="26:67">
              Rede
            </p>
          </div>
        </div>
        <div className="[word-break:break-word] content-stretch flex h-[24px] items-center justify-between leading-[normal] not-italic overflow-clip relative shrink-0 text-[9px] w-full whitespace-nowrap" data-node-id="26:68" data-name="Status">
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[#667893]" data-node-id="26:69">
            7 locais • pasta selecionada
          </p>
          <p className="font-['Inter:Bold'] font-bold relative shrink-0 text-[#7385a2]" data-node-id="26:70">
            Ctrl+F
          </p>
        </div>
      </div>
    </div>
  );
}

function PlayerPlaylist({ className }: { className?: string }) {
  return (
    <div className={className || "h-[400px] relative w-[1010px]"} data-node-id="24:8" data-name="Player/Playlist">
      <div className="absolute inset-[-0.13%_0]">
        <img alt="" className="block max-w-none size-full" src={imgPlayerPlaylist} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[3.75%_80.59%_91.75%_1.98%] leading-[normal] not-italic text-[#f8fafc] text-[15px] whitespace-nowrap" data-node-id="17:482">
        LISTA DE REPRODUÇÃO
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[4.75%_4.75%_92%_87.03%] leading-[normal] not-italic text-[#64748b] text-[11px] text-right whitespace-nowrap" data-node-id="17:483">
        12 itens • 38:42
      </p>
      <div className="absolute inset-[11%_1.19%_81.5%_1.19%]" data-node-id="17:484" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector3} />
      </div>
      <div className="[word-break:break-word] absolute contents font-['Inter:Bold'] font-bold inset-[13.5%_5.15%_83.5%_2.77%] leading-[normal] not-italic text-[#64748b] text-[10px] whitespace-nowrap" data-node-id="17:485" data-name="Group">
        <p className="absolute inset-[13.5%_96.53%_83.5%_2.77%]" data-node-id="17:486">
          #
        </p>
        <p className="absolute inset-[13.5%_91.29%_83.5%_6.34%]" data-node-id="17:487">
          TIPO
        </p>
        <p className="absolute inset-[13.5%_76.14%_83.5%_14.65%]" data-node-id="17:488">
          ARQUIVO / TÍTULO
        </p>
        <p className="absolute inset-[13.5%_31.39%_83.5%_63.56%]" data-node-id="17:489">
          DURAÇÃO
        </p>
        <p className="absolute inset-[13.5%_24.16%_83.5%_72.67%]" data-node-id="17:490">
          INÍCIO
        </p>
        <p className="absolute inset-[13.5%_16.63%_83.5%_81.58%]" data-node-id="17:491">
          FIM
        </p>
        <p className="absolute inset-[13.5%_5.15%_83.5%_90.89%]" data-node-id="17:492">
          STATUS
        </p>
      </div>
      <div className="absolute contents inset-[20%_1.19%_10%_1.19%]" data-node-id="17:493" data-name="Group">
        <div className="absolute inset-[20%_1.19%_68.5%_1.19%]" data-node-id="17:494" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector4} />
        </div>
        <div className="absolute inset-[20%_98.32%_68.5%_1.19%]" data-node-id="17:495" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector5} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[24%_95.84%_72.75%_2.97%] leading-[normal] not-italic text-[#fca5a5] text-[11px] whitespace-nowrap" data-node-id="17:496">
          01
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[24%_89.31%_72.75%_6.34%] leading-[normal] not-italic text-[#fca5a5] text-[11px] whitespace-nowrap" data-node-id="17:497">
          MÚSICA
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[22.25%_73.66%_74.5%_14.65%] leading-[normal] not-italic text-[#f8fafc] text-[11px] whitespace-nowrap" data-node-id="17:498">
          Ed Sheeran — Azizam
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[26.5%_74.85%_70.75%_14.65%] leading-[normal] not-italic text-[#9f6b73] text-[9px] whitespace-nowrap" data-node-id="17:499">
          Pop Internacional • 2025
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[24%_33.37%_72.75%_63.56%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:500">
          03:42
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[24%_22.77%_72.75%_72.67%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:501">
          21:42:50
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[24%_13.86%_72.75%_81.58%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:502">
          21:46:32
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[24%_5.64%_72.75%_90.89%] leading-[normal] not-italic text-[#fca5a5] text-[11px] whitespace-nowrap" data-node-id="17:503">
          NO AR
        </p>
        <div className="absolute inset-[32.5%_1.19%_56%_1.19%]" data-node-id="17:504" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector6} />
        </div>
        <div className="absolute inset-[32.5%_98.32%_56%_1.19%]" data-node-id="17:505" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector7} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[36.5%_95.64%_60.25%_2.97%] leading-[normal] not-italic text-[#6ee7b7] text-[11px] whitespace-nowrap" data-node-id="17:506">
          02
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[36.5%_89.01%_60.25%_6.34%] leading-[normal] not-italic text-[#6ee7b7] text-[11px] whitespace-nowrap" data-node-id="17:507">
          VINHETA
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[36.5%_69.9%_60.25%_14.65%] leading-[normal] not-italic text-[#f8fafc] text-[11px] whitespace-nowrap" data-node-id="17:508">
          VBC — A rádio que toca você
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[36.5%_33.37%_60.25%_63.56%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:509">
          00:08
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[36.5%_22.77%_60.25%_72.67%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:510">
          21:46:32
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[36.5%_13.86%_60.25%_81.58%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:511">
          21:46:40
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[36.5%_3.86%_60.25%_90.89%] leading-[normal] not-italic text-[#6ee7b7] text-[11px] whitespace-nowrap" data-node-id="17:512">
          PRÓXIMO
        </p>
        <div className="absolute inset-[45%_1.19%_44.5%_1.19%]" data-node-id="17:513" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector8} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_95.64%_48%_2.97%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:514">
          03
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_89.31%_48%_6.34%] leading-[normal] not-italic text-[#60a5fa] text-[11px] whitespace-nowrap" data-node-id="17:515">
          MÚSICA
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_69.6%_48%_14.65%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] whitespace-nowrap" data-node-id="17:516">
          The Weeknd — Blinding Lights
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_33.37%_48%_63.56%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:517">
          03:20
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_22.77%_48%_72.67%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:518">
          21:46:40
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_13.86%_48%_81.58%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:519">
          21:50:00
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[48.75%_3.86%_48%_90.89%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:520">
          AGUARDA
        </p>
        <div className="absolute inset-[56.5%_1.19%_33%_1.19%]" data-node-id="17:521" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector9} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_95.64%_36.5%_2.97%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:522">
          04
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_87.23%_36.5%_6.34%] leading-[normal] not-italic text-[#fbbf24] text-[11px] whitespace-nowrap" data-node-id="17:523">
          COMERCIAL
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_72.28%_36.5%_14.65%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] whitespace-nowrap" data-node-id="17:524">
          Bloco comercial — 21h50
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_33.37%_36.5%_63.56%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:525">
          02:30
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_22.77%_36.5%_72.67%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:526">
          21:50:00
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_13.86%_36.5%_81.58%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:527">
          21:52:30
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[60.25%_2.97%_36.5%_90.89%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:528">
          AGENDADO
        </p>
        <div className="absolute inset-[68%_1.19%_21.5%_1.19%]" data-node-id="17:529" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector8} />
        </div>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[2.97%] not-italic right-[95.64%] text-[#64748b] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:530">
          05
        </p>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[6.34%] not-italic right-[88.32%] text-[#a78bfa] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:531">
          LOCUÇÃO
        </p>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[14.65%] not-italic right-[71.09%] text-[#cbd5e1] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:532">
          Chamada — Jornal da noite
        </p>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[63.56%] not-italic right-[33.37%] text-[#94a3b8] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:533">
          00:22
        </p>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[72.67%] not-italic right-[22.77%] text-[#94a3b8] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:534">
          21:52:30
        </p>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[81.58%] not-italic right-[13.96%] text-[#94a3b8] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:535">
          21:52:52
        </p>
        <p className="[word-break:break-word] absolute bottom-1/4 font-['Inter:Regular'] font-normal leading-[normal] left-[90.89%] not-italic right-[3.86%] text-[#64748b] text-[11px] top-[71.75%] whitespace-nowrap" data-node-id="17:536">
          AGUARDA
        </p>
        <div className="absolute inset-[79.5%_1.19%_10%_1.19%]" data-node-id="17:537" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector9} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_95.64%_13.5%_2.97%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:538">
          06
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_89.31%_13.5%_6.34%] leading-[normal] not-italic text-[#60a5fa] text-[11px] whitespace-nowrap" data-node-id="17:539">
          MÚSICA
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_75.15%_13.5%_14.65%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] whitespace-nowrap" data-node-id="17:540">
          Dua Lipa — Houdini
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_33.37%_13.5%_63.56%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:541">
          03:05
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_22.87%_13.5%_72.67%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:542">
          21:52:52
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_13.96%_13.5%_81.58%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:543">
          21:55:57
        </p>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[83.25%_3.86%_13.5%_90.89%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:544">
          AGUARDA
        </p>
      </div>
      <div className="absolute inset-[92%_86.53%_1.5%_1.98%]" data-node-id="17:545" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector10} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[94%_88.96%_3%_4.41%] leading-[normal] not-italic text-[10px] text-center text-white whitespace-nowrap" data-node-id="17:546">
        + ADICIONAR
      </p>
      <div className="absolute inset-[92%_77.23%_1.5%_14.26%]" data-node-id="17:547" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector11} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[94%_79.11%_3%_16.14%] leading-[normal] not-italic text-[#cbd5e1] text-[10px] text-center whitespace-nowrap" data-node-id="17:548">
        REMOVER
      </p>
      <div className="absolute inset-[92%_66.73%_1.5%_23.56%]" data-node-id="17:549" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector12} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[94%_67.87%_3%_24.7%] leading-[normal] not-italic text-[#cbd5e1] text-[10px] text-center whitespace-nowrap" data-node-id="17:550">
        PROPRIEDADES
      </p>
    </div>
  );
}

function PlayerPlaybackModes({ className }: { className?: string }) {
  return (
    <div className={className || "h-[236px] relative w-[328px]"} data-node-id="24:7" data-name="Player/Playback Modes">
      <div className="absolute inset-[-0.21%_-0.15%]">
        <img alt="" className="block max-w-none size-full" src={imgPlayerPlaybackModes} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[6.36%_53.35%_88.14%_6.1%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:461">
        MODO DE REPRODUÇÃO
      </p>
      <div className="absolute inset-[18.64%_51.22%_59.32%_6.1%]" data-node-id="17:462" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector13} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[23.73%_59.76%_69.92%_14.63%] leading-[normal] not-italic text-[12px] text-center text-white whitespace-nowrap" data-node-id="17:463">
        AUTOMÁTICO
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[31.78%_59.91%_63.56%_14.79%] leading-[normal] not-italic text-[#bfdbfe] text-[9px] text-center whitespace-nowrap" data-node-id="17:464">
        sequência contínua
      </p>
      <div className="absolute inset-[18.64%_6.1%_59.32%_51.22%]" data-node-id="17:465" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector14} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[23.73%_19.21%_69.92%_64.33%] leading-[normal] not-italic text-[#cbd5e1] text-[12px] text-center whitespace-nowrap" data-node-id="17:466">
        MANUAL
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[31.78%_13.72%_63.56%_58.84%] leading-[normal] not-italic text-[#64748b] text-[9px] text-center whitespace-nowrap" data-node-id="17:467">
        controle do operador
      </p>
      <div className="absolute inset-[46.61%_6.1%_34.75%_6.1%]" data-node-id="17:468" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector15} />
      </div>
      <p className="[word-break:break-word] absolute bottom-[44.92%] font-['Inter:Regular'] font-normal leading-[normal] left-[10.98%] not-italic right-[71.04%] text-[#64748b] text-[10px] top-1/2 whitespace-nowrap" data-node-id="17:469">
        CROSSFADE
      </p>
      <p className="[word-break:break-word] absolute bottom-[41.53%] font-['Arial:Bold'] leading-[normal] left-3/4 not-italic right-[14.02%] text-[#f8fafc] text-[16px] text-right top-[50.85%] whitespace-nowrap" data-node-id="17:470">
        2.5 s
      </p>
      <div className="absolute inset-[58.9%_34.15%_39.41%_10.98%]" data-node-id="17:471" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector16} />
      </div>
      <div className="absolute inset-[58.9%_60.37%_39.41%_10.98%]" data-node-id="17:472" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector17} />
      </div>
      <div className="absolute inset-[57.2%_58.54%_37.71%_37.8%]" data-node-id="17:473" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector18} />
      </div>
      <div className="absolute inset-[71.19%_65.85%_10.17%_6.1%]" data-node-id="17:474" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector19} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[78.39%_75.76%_16.53%_16.01%] leading-[normal] not-italic text-[#94a3b8] text-[10px] text-center whitespace-nowrap" data-node-id="17:475">
        LOOP
      </p>
      <div className="absolute inset-[71.19%_35.98%_10.17%_35.98%]" data-node-id="17:476" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector19} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[78.39%_41.62%_16.53%_41.62%] leading-[normal] not-italic text-[#94a3b8] text-[10px] text-center whitespace-nowrap" data-node-id="17:477">
        ALEATÓRIO
      </p>
      <div className="absolute inset-[71.19%_6.1%_10.17%_65.85%]" data-node-id="17:478" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector19} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[78.39%_13.11%_16.53%_72.87%] leading-[normal] not-italic text-[#94a3b8] text-[10px] text-center whitespace-nowrap" data-node-id="17:479">
        SATÉLITE
      </p>
    </div>
  );
}

function PlayerStudioClockMeters({ className }: { className?: string }) {
  return (
    <div className={className || "relative size-[236px]"} data-node-id="24:6" data-name="Player/Studio Clock & Meters">
      <div className="absolute inset-[-0.21%]">
        <img alt="" className="block max-w-none size-full" src={imgPlayerStudioClockMeters} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[6.36%_47.88%_88.14%_8.47%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:446">
        HORA DO ESTÚDIO
      </p>
      <p className="[word-break:break-word] absolute font-['Arial:Bold'] inset-[15.25%_16.53%_63.14%_8.47%] leading-[normal] not-italic text-[#f8fafc] text-[44px] whitespace-nowrap" data-node-id="17:447">
        21:44:14
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[40.25%_24.15%_53.39%_8.47%] leading-[normal] not-italic text-[#94a3b8] text-[12px] whitespace-nowrap" data-node-id="17:448">
        Terça-feira, 22 de setembro
      </p>
      <div className="absolute inset-[54.24%_8.47%_45.76%_8.47%]" data-node-id="17:449" data-name="Vector">
        <div className="absolute inset-[-0.5px_0]">
          <img alt="" className="block max-w-none size-full" src={imgVector20} />
        </div>
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[61.86%_88.98%_33.05%_8.47%] leading-[normal] not-italic text-[#64748b] text-[10px] whitespace-nowrap" data-node-id="17:450">
        L
      </p>
      <div className="absolute inset-[61.44%_14.41%_33.47%_16.95%]" data-node-id="17:451" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector21} />
      </div>
      <div className="absolute inset-[61.44%_28.54%_33.47%_16.95%]" data-node-id="17:452" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector22} />
      </div>
      <div className="absolute inset-[61.44%_19.92%_33.47%_70.34%]" data-node-id="17:453" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector23} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[73.73%_88.56%_21.19%_8.47%] leading-[normal] not-italic text-[#64748b] text-[10px] whitespace-nowrap" data-node-id="17:454">
        R
      </p>
      <div className="absolute inset-[73.31%_14.41%_21.61%_16.95%]" data-node-id="17:455" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector21} />
      </div>
      <div className="absolute inset-[73.31%_32.63%_21.61%_16.95%]" data-node-id="17:456" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector24} />
      </div>
      <div className="absolute inset-[73.31%_25.42%_21.61%_66.95%]" data-node-id="17:457" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector25} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[87.29%_58.05%_7.63%_8.47%] leading-[normal] not-italic text-[#64748b] text-[10px] whitespace-nowrap" data-node-id="17:458">
        MASTER -4.2 dB
      </p>
    </div>
  );
}

function PlayerDeckNext({ className }: { className?: string }) {
  return (
    <div className={className || "h-[236px] relative w-[396px]"} data-node-id="24:5" data-name="Player/Deck/Next">
      <div className="absolute inset-[-0.21%_-0.13%]">
        <img alt="" className="block max-w-none size-full" src={imgPlayerDeckNext} />
      </div>
      <div className="[word-break:break-word] absolute bg-[#1e293b] inset-[52.12%_48.23%_9.75%_4.29%] leading-[normal] not-italic overflow-clip rounded-[11px]" data-node-id="29:37">
        <p className="absolute font-['Inter:Regular'] font-normal inset-[7.78%_41.87%_77.78%_4.86%] text-[#94a3b8] text-[11px]" data-node-id="29:38">{`Duração `}</p>
        <p className="absolute font-['Arial:Bold'] inset-[27.78%_5.56%_11.11%_5.85%] text-[#f8fafc] text-[48px]" data-node-id="29:39">
          00:10.0
        </p>
      </div>
      <div className="absolute inset-[0_0_83.9%_0]" data-node-id="17:433" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector26} />
      </div>
      <div className="absolute inset-[10.17%_0_83.9%_0]" data-node-id="17:434" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector27} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[5.08%_69.95%_88.14%_5.56%] leading-[normal] not-italic text-[13px] text-white whitespace-nowrap" data-node-id="17:435">
        PRÓXIMO ITEM
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[22.03%_32.32%_65.68%_5.05%] leading-[normal] not-italic text-[#f8fafc] text-[24px] whitespace-nowrap" data-node-id="17:436">
        Vinheta — VBC 2026
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[38.14%_39.39%_55.51%_5.05%] leading-[normal] not-italic text-[#64748b] text-[12px] whitespace-nowrap" data-node-id="17:437">
        Vinheta • INSTITUCIONAL • ID 000127
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[53.81%_21.21%_40.68%_56.06%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:440">
        INÍCIO PREVISTO
      </p>
      <p className="[word-break:break-word] absolute font-['Arial:Bold'] inset-[63.98%_18.43%_23.73%_56.06%] leading-[normal] not-italic text-[#e2e8f0] text-[25px] whitespace-nowrap" data-node-id="17:441">
        21:48:50
      </p>
      <div className="absolute inset-[82.2%_6.57%_5.93%_56.06%]" data-node-id="17:442" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector28} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[85.59%_19.32%_8.9%_68.81%] leading-[normal] not-italic text-[#6ee7b7] text-[11px] text-center whitespace-nowrap" data-node-id="17:443">
        PRONTO
      </p>
    </div>
  );
}

function PlayerDeckOnAir({ className }: { className?: string }) {
  return (
    <div className={className || "h-[236px] relative w-[396px]"} data-node-id="24:4" data-name="Player/Deck/On Air">
      <div className="absolute inset-[-0.21%_-0.13%]">
        <img alt="" className="block max-w-none size-full" src={imgPlayerDeckNext} />
      </div>
      <div className="absolute inset-[0_0_83.9%_0]" data-node-id="17:418" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector29} />
      </div>
      <div className="absolute inset-[10.17%_0_83.9%_0]" data-node-id="17:419" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector30} />
      </div>
      <div className="absolute inset-[5.08%_92.17%_88.98%_4.29%]" data-node-id="17:420" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector31} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[4.66%_44.44%_88.56%_10.61%] leading-[normal] not-italic text-[13px] text-white whitespace-nowrap" data-node-id="17:421">
        NO AR — TOCANDO AGORA
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[22.03%_30.05%_65.68%_5.05%] leading-[normal] not-italic text-[#f8fafc] text-[24px] whitespace-nowrap" data-node-id="17:422">
        Ed Sheeran — Azizam
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[38.14%_31.82%_55.51%_5.05%] leading-[normal] not-italic text-[#64748b] text-[12px] whitespace-nowrap" data-node-id="17:423">
        Música • POP INTERNACIONAL • ID 001842
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[53.81%_19.44%_40.68%_63.64%] leading-[normal] not-italic text-[#94a3b8] text-[11px] whitespace-nowrap" data-node-id="17:426">
        TERMINA ÀS
      </p>
      <p className="[word-break:break-word] absolute font-['Arial:Bold'] inset-[62.29%_10.86%_25.42%_63.64%] leading-[normal] not-italic text-[#e2e8f0] text-[25px] whitespace-nowrap" data-node-id="17:427">
        21:46:32
      </p>
      <div className="absolute inset-[79.66%_6.57%_16.95%_63.64%]" data-node-id="17:428" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector32} />
      </div>
      <div className="absolute inset-[79.66%_17.68%_16.95%_63.64%]" data-node-id="17:429" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector33} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[87.29%_18.18%_7.63%_63.64%] leading-[normal] not-italic text-[#64748b] text-[10px] whitespace-nowrap" data-node-id="17:430">
        Progresso 63%
      </p>
      <div className="[word-break:break-word] absolute bg-[#1e293b] inset-[51.69%_48.99%_10.17%_3.54%] leading-[normal] not-italic overflow-clip rounded-[11px]" data-node-id="29:22">
        <p className="absolute font-['Inter:Regular'] font-normal inset-[7.78%_41.87%_77.78%_4.86%] text-[#94a3b8] text-[11px]" data-node-id="17:424">
          TEMPO RESTANTE
        </p>
        <p className="absolute font-['Arial:Bold'] inset-[27.78%_5.56%_11.11%_5.85%] text-[#f8fafc] text-[48px]" data-node-id="17:425">
          02:18.4
        </p>
      </div>
      <div className="[word-break:break-word] absolute bg-[#1e293b] inset-[51.69%_48.99%_10.17%_3.54%] leading-[normal] not-italic overflow-clip rounded-[11px]" data-node-id="29:23">
        <p className="absolute font-['Inter:Regular'] font-normal inset-[7.78%_41.87%_77.78%_4.86%] text-[#94a3b8] text-[11px]" data-node-id="29:24">
          TEMPO RESTANTE
        </p>
        <p className="absolute font-['Arial:Bold'] inset-[27.78%_5.56%_11.11%_5.85%] text-[#f8fafc] text-[48px]" data-node-id="29:25">
          02:18.4
        </p>
      </div>
      <div className="[word-break:break-word] absolute bg-[#1e293b] inset-[51.69%_48.99%_10.17%_3.54%] leading-[normal] not-italic overflow-clip rounded-[11px]" data-node-id="29:33">
        <p className="absolute font-['Inter:Regular'] font-normal inset-[7.78%_41.87%_77.78%_4.86%] text-[#94a3b8] text-[11px]" data-node-id="29:34">
          TEMPO RESTANTE
        </p>
        <p className="absolute font-['Arial:Bold'] inset-[27.78%_5.56%_11.11%_5.85%] text-[#f8fafc] text-[48px]" data-node-id="29:35">
          02:18.4
        </p>
      </div>
    </div>
  );
}

function PlayerToolbar({ className }: { className?: string }) {
  return (
    <div className={className || "h-[58px] relative w-[1440px]"} data-node-id="24:3" data-name="Player/Toolbar">
      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgPlayerToolbar} />
      <div className="absolute contents inset-[20.69%_57.08%_20.69%_1.25%]" data-node-id="17:397" data-name="Group">
        <div className="absolute inset-[20.69%_92.92%_20.69%_1.25%]" data-node-id="17:398" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector34} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_94.03%_37.93%_2.36%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] text-center whitespace-nowrap" data-node-id="17:399">
          Nova lista
        </p>
        <div className="absolute inset-[20.69%_86.53%_20.69%_7.64%]" data-node-id="17:400" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector34} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_88.54%_37.93%_9.65%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] text-center whitespace-nowrap" data-node-id="17:401">
          Abrir
        </p>
        <div className="absolute inset-[20.69%_80.14%_20.69%_14.03%]" data-node-id="17:402" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector34} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_81.91%_37.93%_15.8%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] text-center whitespace-nowrap" data-node-id="17:403">
          Salvar
        </p>
        <div className="absolute inset-[20.69%_72.08%_20.69%_20.97%]" data-node-id="17:404" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector35} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_73.54%_37.93%_22.43%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] text-center whitespace-nowrap" data-node-id="17:405">
          Agendador
        </p>
        <div className="absolute inset-[20.69%_64.58%_20.69%_28.47%]" data-node-id="17:406" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector35} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_66.6%_37.93%_30.49%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] text-center whitespace-nowrap" data-node-id="17:407">
          Eventos
        </p>
        <div className="absolute inset-[20.69%_57.08%_20.69%_35.97%]" data-node-id="17:408" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector35} />
        </div>
        <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_58.75%_37.93%_37.64%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] text-center whitespace-nowrap" data-node-id="17:409">
          Relatórios
        </p>
      </div>
      <div className="absolute inset-[20.69%_12.92%_20.69%_78.33%]" data-node-id="17:410" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector36} />
      </div>
      <div className="absolute inset-[41.38%_19.93%_41.38%_79.38%]" data-node-id="17:411" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector37} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_14.72%_37.93%_80.69%] leading-[normal] not-italic text-[#cbd5e1] text-[11px] whitespace-nowrap" data-node-id="17:412">
        AUTO ATIVO
      </p>
      <div className="absolute inset-[20.69%_1.25%_20.69%_87.64%]" data-node-id="17:413" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector38} />
      </div>
      <p className="[word-break:break-word] absolute font-['Inter:Regular'] font-normal inset-[39.66%_8.89%_37.93%_88.89%] leading-[normal] not-italic text-[#64748b] text-[11px] whitespace-nowrap" data-node-id="17:414">
        Saída:
      </p>
      <p className="[word-break:break-word] absolute font-['Inter:Bold'] font-bold inset-[39.66%_2.22%_37.93%_91.67%] leading-[normal] not-italic text-[#e2e8f0] text-[11px] whitespace-nowrap" data-node-id="17:415">
        REALTEK AUDIO
      </p>
    </div>
  );
}

function PlayerHeader({ className }: { className?: string }) {
  return (
    <div className={className || "h-[48px] relative w-[1440px]"} data-node-id="24:2" data-name="Player/Header">
      <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgPlayerHeader} />
      <div className="absolute inset-[66.67%_0_0_0]" data-node-id="17:386" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector39} />
      </div>
      <p className="[word-break:break-word] absolute bottom-[18.75%] font-['Inter:Regular'] font-normal leading-[normal] left-[7.99%] not-italic right-[82.5%] text-[#64748b] text-[12px] top-1/2 whitespace-nowrap" data-node-id="17:391">
        AUTOMAÇÃO DE RÁDIO
      </p>
      <div className="absolute inset-[33.33%_1.25%_34.38%_97.57%]" data-node-id="56:292" data-name="Vector">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector40} />
      </div>
      <div className="absolute inset-[47.92%_9.41%_46.88%_89.1%]" data-node-id="56:304">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector41} />
      </div>
    </div>
  );
}

export default function VbcPlayerAutomacaoDeRadio() {
  return (
    <div className="relative size-full" data-node-id="16:157" data-name="VBC Player - Automacao de Radio">
      <div className="absolute inset-0 overflow-clip" data-node-id="17:382" data-name="VBC Player - Grupos Editaveis">
        <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVbcPlayerGruposEditaveis} />
        <PlayerHeader className="absolute inset-[0_0_94.67%_0]" />
        <PlayerToolbar className="absolute inset-[5.33%_0_88.22%_0]" />
        <PlayerDeckOnAir className="absolute inset-[13.56%_71.25%_60.22%_1.25%]" />
        <PlayerDeckNext className="absolute inset-[13.56%_42.64%_60.22%_29.86%]" />
        <PlayerStudioClockMeters className="absolute inset-[13.56%_25.14%_60.22%_58.47%]" />
        <PlayerPlaybackModes className="absolute inset-[13.56%_1.25%_60.22%_75.97%]" />
        <PlayerPlaylist className="absolute inset-[41.56%_28.61%_14%_1.25%]" />
        <PlayerFileExplorer className="absolute bg-[#111a2a] border border-[#26344a] border-solid content-stretch flex flex-col inset-[41.56%_1.25%_14%_72.5%] items-start overflow-clip rounded-[12px]" />
        <PlayerTransport className="absolute inset-[87.78%_1.25%_2%_1.25%]" />
        <div className="-translate-y-1/2 absolute aspect-[1049/570] left-[0.83%] overflow-clip right-[92.78%] top-[calc(50%-412px)]" data-node-id="29:6" data-name="Logo VBC / Cores originais iluminadas">
          <div className="absolute inset-[3.68%_71.21%_33.68%_1.91%]" data-node-id="29:7" data-name="V / Azul-marinho">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVAzulMarinho} />
          </div>
          <div className="absolute inset-[3.68%_60.82%_61.58%_18.02%]" data-node-id="29:8" data-name="V / Ciano">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVCiano} />
          </div>
          <div className="absolute inset-[3.68%_32.79%_33.68%_41.66%]" data-node-id="29:9" data-name="B / Azul">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgBAzul} />
          </div>
          <div className="absolute inset-[3.68%_37.94%_33.68%_41.66%]" data-node-id="29:10" data-name="B / Azul-marinho">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgBAzulMarinho} />
          </div>
          <div className="absolute inset-[3.77%_1.91%_34.13%_69.52%]" data-node-id="29:11" data-name="C / Azul-marinho">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgCAzulMarinho} />
          </div>
          <div className="absolute inset-[3.77%_1.95%_65%_74.55%]" data-node-id="29:12" data-name="C / Ciano">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgCCiano} />
          </div>
        </div>
        <div className="absolute inset-[1.78%_5.28%_96.44%_93.54%]" data-node-id="56:298" data-name="Vector">
          <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgVector42} />
        </div>
      </div>
    </div>
  );
}
